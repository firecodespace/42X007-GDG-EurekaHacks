from fastapi import APIRouter
from app.services.match_service import match_team

router = APIRouter()

@router.post("/")
def generate_team(payload: dict):
    return match_team(payload["users"], payload["event"])
