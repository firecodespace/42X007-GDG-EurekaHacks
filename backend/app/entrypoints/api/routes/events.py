from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_events():
    return {
        "items": [],
        "message": "Stub: next step will read from Firestore."
    }
