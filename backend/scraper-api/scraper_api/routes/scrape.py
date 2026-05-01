import logging

from fastapi import APIRouter, Depends

from scraper_api.dependencies import get_scraper
from scraper_api.schema import ScrapeRequest, ScrapeResult
from scraper_api.scraper import PlaywrightScraper


router = APIRouter(prefix="/scrape", tags=["scrape"])
logger = logging.getLogger(__name__)


@router.post("", response_model=ScrapeResult)
async def scrape(
    request: ScrapeRequest,
    scraper: PlaywrightScraper = Depends(get_scraper),
) -> ScrapeResult:
    logger.info(f"Scrape request for: {request.url}")
    return await scraper.scrape(request.url)
