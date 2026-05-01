import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scraper_api.config import get_settings
from scraper_api.logging_config import configure_logging
from scraper_api.routes.scrape import router as scrape_router
from scraper_api.scraper import PlaywrightScraper


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
    return {"status": "healthy", "service": "scraper"}


def main() -> None:
    uvicorn.run(
        "scraper_api.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=False,
    )
