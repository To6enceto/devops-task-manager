import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import json as json_logger
from sqlalchemy import func, select, text

from app.config import settings
from app.database import engine, get_db
from app.models import Base, Task
from app.routers import tasks

# --- Structured JSON Logging ---
logger = logging.getLogger("task_manager")
handler = logging.StreamHandler(sys.stdout)
formatter = json_logger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={"asctime": "timestamp", "levelname": "level"},
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(settings.log_level)


# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application", extra={"app": settings.app_name})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting down application")
    await engine.dispose()


# --- App ---
app = FastAPI(
    title=settings.app_name,
    description="A CRUD Task Manager showcasing a full DevOps lifecycle.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Prometheus Metrics ---
Instrumentator(
    should_group_status_codes=True,
    excluded_handlers=["/health", "/ready", "/metrics"],
).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# --- Routers ---
app.include_router(tasks.router)


# --- Health Checks ---
@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}


@app.get("/ready", tags=["health"])
async def readiness():
    try:
        async for db in get_db():
            await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        logger.exception("Readiness check failed")
        return {"status": "not ready"}, 503


@app.get("/", tags=["root"])
async def root():
    return {
        "app": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
    }
