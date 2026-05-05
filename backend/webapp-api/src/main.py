import logging
import re
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from sqlalchemy import text

import lib.db.schema_registry  # noqa: F401 - Ensures all SQLAlchemy models are registered
from lib.db.database import engine
from lib.scraper.playwright_scraper import PlaywrightScraper
from lib.supabase_client.storage.service import SupabaseStorageService
from src.brand.routes import router as brand_router
from src.brand_generation_job.routes import router as brand_generation_router
from src.config import get_settings
from src.docs import router as docs_router
from src.http_logging import http_logging_middleware
from src.logging_config import configure_logging


logger = logging.getLogger(__name__)


settings = get_settings()

configure_logging(
    level=settings.log_level,
    service_name="api",
    environment=settings.environment,
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting Playwright browser")
    storage_service = SupabaseStorageService()
    scraper = PlaywrightScraper(storage_service=storage_service)
    await scraper.start()
    application.state.playwright_scraper = scraper
    logger.info("Playwright browser ready")
    yield
    logger.info("Shutting down Playwright browser")
    await scraper.stop()


def _operation_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    tag_slug = re.sub(r"[\s\-]+", "_", tag).lower()
    return f"{tag_slug}_{route.name}"


app = FastAPI(
    title="Voz AI API",
    description="Voz AI marketing automation platform API",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    redirect_slashes=False,
    generate_unique_id_function=_operation_id,
    lifespan=lifespan,
)

app.middleware("http")(http_logging_middleware)

allowed_origins = [
    "https://vozai.pages.dev",
]

if settings.environment == "development":
    allowed_origins.extend(
        [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(docs_router)
app.include_router(brand_router)
app.include_router(brand_generation_router)


@app.get("/health")
async def health_check():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception as error:
        logger.error("Database readiness probe failed: %s", error)
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "reason": "database unreachable"},
        )
    return {"status": "ok", "environment": settings.environment}


@app.get("/")
async def root():
    return {
        "message": "Voz AI API",
        "version": "0.1.0",
        "docs": "/docs",
    }


def main():
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    main()
