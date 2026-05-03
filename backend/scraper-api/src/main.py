import logging
from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.logging_config import configure_logging
from src.routes.scrape import router as scrape_router
from src.scraper import PlaywrightScraper


settings = get_settings()

configure_logging(level=settings.log_level, service_name="scraper-api")

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Playwright browser")
    scraper = PlaywrightScraper()
    await scraper._ensure_browser()
    app.state.scraper = scraper
    logger.info("Playwright browser ready")
    yield
    logger.info("Shutting down Playwright browser")
    await scraper._cleanup()


app = FastAPI(
    title="Voz AI Scraper Service",
    description="Playwright-based web scraping service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scrape_router)


@app.get("/health")
async def health():
    webapp_api_url = settings.webapp_api_url
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{webapp_api_url}/health")
            response.raise_for_status()
    except Exception as error:
        logger.error("webapp-api readiness probe failed: %s", error)
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "reason": "webapp-api unreachable"},
        )
    return {"status": "healthy", "service": "scraper"}


def main() -> None:
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=False,
    )
