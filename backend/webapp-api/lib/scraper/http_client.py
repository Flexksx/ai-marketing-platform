import logging

import httpx
import public

from src.config import get_settings
from scraper_api_contract.scraper import ScrapeResult


logger = logging.getLogger(__name__)


@public.add
class HttpScraperClient:
    """Calls the scraper-api service over HTTP."""

    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.scraper_service_url.rstrip("/")

    async def scrape_async(self, url: str) -> ScrapeResult:
        logger.info(f"Delegating scrape to scraper-api: {url}")
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self._base_url}/scrape",
                json={"url": url},
            )
            response.raise_for_status()
            return ScrapeResult.model_validate(response.json())
