# backend/app/services/fire_service.py
import logging
import json
from typing import List, Dict

LOG = logging.getLogger("fire_service")
LOG.setLevel(logging.INFO)

try:
    from app.config.firebase_init import db  # if you later enable firebase_init, it should expose `db`
    FIRESTORE_ENABLED = True
except Exception:
    db = None
    FIRESTORE_ENABLED = False
    LOG.info("Firestore not configured; run in mock mode")

def save_events_to_firestore(events: List[Dict], collection: str = "competitions"):
    if not FIRESTORE_ENABLED or db is None:
        LOG.info("Firestore disabled: writing to local file instead")
        # fallback: write to a local JSON so frontend devs can use it
        with open("public/mock/gdg_events.json", "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        return {"status": "mock_saved", "count": len(events)}

    # If firestore is configured, do batch writes
    batch = db.batch()
    coll_ref = db.collection(collection)
    for ev in events:
        doc_ref = coll_ref.document()  # auto id
        batch.set(doc_ref, ev)
    batch.commit()
    LOG.info("Saved %d events to Firestore collection %s", len(events), collection)
    return {"status": "saved", "count": len(events)}
