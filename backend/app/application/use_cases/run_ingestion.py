from dataclasses import dataclass
from typing import Optional

from app.adapters.discovery.unstop_discoverer import UnstopDiscoverer
from app.application.pipeline.ingestion_pipeline import EventIngestionPipeline
from app.adapters.persistence.firestore.run_store import create_run, finish_run


@dataclass
class RunResult:
    run_id: str
    events_count: int
    error: Optional[str] = None


def run_ingestion_once(max_events: int = 20) -> RunResult:
    run = create_run(source="unstop", max_events=max_events)
    try:
        discoverer = UnstopDiscoverer()
        pipeline = EventIngestionPipeline(discoverer=discoverer, max_events=max_events)
        events = pipeline.run()
        finish_run(run.run_id, events_count=len(events), error=None)
        return RunResult(run_id=run.run_id, events_count=len(events), error=None)
    except Exception as exc:
        finish_run(run.run_id, events_count=0, error=str(exc))
        raise  # IMPORTANT: show full traceback in terminal
