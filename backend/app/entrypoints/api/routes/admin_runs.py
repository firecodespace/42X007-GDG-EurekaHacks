from fastapi import APIRouter
import subprocess
import sys

router = APIRouter()

_running = False
_last = {"running": False, "last_run_id": None, "last_error": "", "last_events_count": 0}


@router.post("/run-once")
def run_once():
    global _running, _last

    if _running:
        return {"queued": False, "message": "Already running", "state": _last}

    _running = True
    _last["running"] = True
    _last["last_error"] = ""

    try:
        # This runs ingestion in a fresh python process so Playwright can spawn safely.
        # You already have: backend/app/dev/run_once.py
        proc = subprocess.run(
            [sys.executable, "-m", "app.dev.run_once"],
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            _last["last_error"] = (proc.stderr or proc.stdout or "").strip()
            _last["last_events_count"] = 0
            return {"queued": False, "state": _last}

        # If run_once.py prints something, return it for debugging
        return {"queued": False, "state": _last, "output": (proc.stdout or "").strip()}
    finally:
        _running = False
        _last["running"] = False


@router.get("/run-status")
def run_status():
    return _last
