from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_competitions():
    return {"message": "Competitions endpoint working"}
