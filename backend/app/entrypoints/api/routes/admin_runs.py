from fastapi import APIRouter

router = APIRouter()

@router.post("/run-once")
def run_once_trigger():
    return {
        "queued": False,
        "message": "Stub: next step will call the ingestion use-case and persist run metadata."
    }
