from fastapi import FastAPI

from app.entrypoints.api.routes.health import router as health_router
from app.entrypoints.api.routes.admin_runs import router as admin_runs_router
from app.entrypoints.api.routes.events import router as events_router


def create_app() -> FastAPI:
    app = FastAPI(title="Event Discovery Backend")

    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(admin_runs_router, prefix="/admin", tags=["admin"])
    app.include_router(events_router, prefix="/events", tags=["events"])

    return app
