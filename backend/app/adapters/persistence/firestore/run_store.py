from dataclasses import asdict, dataclass
from typing import Optional
from uuid import uuid4

from app.adapters.persistence.firestore.client import get_firestore_client


@dataclass
class RunRecord:
    run_id: str
    status: str
    source: str
    max_events: int
    events_count: Optional[int] = None
    error: Optional[str] = None


def create_run(source: str, max_events: int) -> RunRecord:
    run_id = uuid4().hex
    rec = RunRecord(run_id=run_id, status="started", source=source, max_events=max_events)
    db = get_firestore_client()
    db.collection("runs").document(run_id).set(asdict(rec))
    return rec


def finish_run(run_id: str, events_count: int, error: Optional[str] = None) -> None:
    db = get_firestore_client()
    status = "failed" if error else "finished"
    db.collection("runs").document(run_id).set(
        {"status": status, "events_count": events_count, "error": error},
        merge=True,
    )
