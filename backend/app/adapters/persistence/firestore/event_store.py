from dataclasses import asdict
from typing import Optional

from google.cloud import firestore

from app.domain.entities.event import Event
from app.adapters.persistence.firestore.client import get_firestore_client


class FirestoreEventStore:
    def __init__(self, collection: str = "events"):
        self.db = get_firestore_client()
        self.collection = collection

    def upsert(self, event: Event, source: str, url: str) -> str:
        # Prefer a stable id if Event has one; otherwise derive from URL
        doc_id = getattr(event, "id", None) or url.split("/")[-1]
        payload = asdict(event) if hasattr(event, "__dataclass_fields__") else event.__dict__.copy()

        payload.update(
            {
                "source": source,
                "source_url": url,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
        )

        self.db.collection(self.collection).document(doc_id).set(payload, merge=True)
        return doc_id
