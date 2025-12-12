from fastapi import FastAPI
from app.api import competitions, match, profile, health

app = FastAPI()

app.include_router(competitions.router, prefix="/competitions")
app.include_router(match.router, prefix="/match")
app.include_router(profile.router, prefix="/profile")
app.include_router(health.router, prefix="/health")
