from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db.schema_registry  # noqa: F401 - Ensures all SQLAlchemy models are registered
from db.schema_init import ensure_schema
from services.worker_api.routes.brand_generation_tasks import (
    router as brand_generation_tasks_router,
)
from services.worker_api.routes.campaign_generation_tasks import (
    router as campaign_generation_tasks_router,
)
from services.worker_api.routes.content_generation_tasks import (
    router as content_generation_tasks_router,
)
from vozai.config import get_settings
from vozai.http_logging import http_logging_middleware
from vozai.logging_config import configure_logging
from vozai.telemetry import setup_telemetry


settings = get_settings()

configure_logging(
    level=settings.log_level,
    service_name="worker-api",
    environment=settings.environment,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_schema(settings.environment)
    yield


app = FastAPI(
    title="Vozai Worker Service",
    description="Background job processing service for campaign and post generation",
    version="1.0.0",
    lifespan=lifespan,
)

app.middleware("http")(http_logging_middleware)

setup_telemetry(app, service_name="worker-api", environment=settings.environment)

app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brand_generation_tasks_router)
app.include_router(campaign_generation_tasks_router)
app.include_router(content_generation_tasks_router)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "worker"}


@app.get("/")
async def root():
    return {
        "service": "Vozai Worker",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/tasks/brand-generation",
            "/tasks/campaign-generation",
            "/tasks/content-generation",
            "/tasks/post-generation",
        ],
    }
