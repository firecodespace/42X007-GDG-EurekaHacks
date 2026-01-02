from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from google.cloud import firestore
from app.adapters.persistence.firestore.client import get_firestore_client

db = get_firestore_client()

def claim_next_url(worker_id: str, source: str = "unstop", lease_seconds: int = 300) -> Optional[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    lease_until = now + timedelta(seconds=lease_seconds)

    # Query a small batch of candidates (Firestore doesn't support "FOR UPDATE" style locks)
    candidates = (
        db.collection("url_frontier")
        .where("source", "==", source)
        .where("status", "==", "pending")
        .limit(10)
        .stream()
    )

    for doc in candidates:
        doc_ref = doc.reference

        @firestore.transactional
        def _txn_claim(txn):
            snap = doc_ref.get(transaction=txn)
            if not snap.exists:
                return None
            data = snap.to_dict() or {}
            locked_until = data.get("locked_until")

            # If locked_until exists and is in the future, skip
            if locked_until and locked_until.replace(tzinfo=timezone.utc) > now:
                return None

            txn.update(
                doc_ref,
                {
                    "status": "in_progress",
                    "locked_until": lease_until,
                    "worker_id": worker_id,
                    "attempts": int(data.get("attempts", 0)) + 1,
                    "last_error": "",
                    "updated_at": firestore.SERVER_TIMESTAMP,
                },
            )
            data["id"] = snap.id
            return data

        txn = db.transaction()
        claimed = _txn_claim(txn)
        if claimed:
            return claimed

    return None
