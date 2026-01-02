from fastapi import APIRouter

from app.application.use_cases.run_ingestion import run_ingestion_once

router = APIRouter()

_running = False
_last = {"running": False, "last_run_id": None, "last_error": None, "last_events_count": None}


@router.post("/run-once")
def run_once():
    global _running, _last

    if _running:
        return {"queued": False, "message": "Already running", "state": _last}

    _running = True
    _last["running"] = True

    try:
        res = run_ingestion_once(max_events=20)
        _last["last_run_id"] = res.run_id
        _last["last_events_count"] = res.events_count
        _last["last_error"] = res.error
        return {"queued": True, "state": _last}
    finally:
        _running = False
        _last["running"] = False


@router.get("/run-status")
def run_status():
    return _last
