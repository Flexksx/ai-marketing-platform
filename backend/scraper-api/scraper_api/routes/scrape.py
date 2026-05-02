import asyncio
import logging

import httpx
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from scraper_api.dependencies import get_scraper
from scraper_api.schema import ScrapeRequest, ScrapeResult
from scraper_api.scraper import PlaywrightScraper


router = APIRouter(prefix="/scrape", tags=["scrape"])
logger = logging.getLogger(__name__)

CALLBACK_SECRET_HEADER = "X-Callback-Secret"

_background_tasks: set[asyncio.Task] = set()


@router.post("", response_model=ScrapeResult)
async def scrape(
    request: ScrapeRequest,
    scraper: PlaywrightScraper = Depends(get_scraper),
) -> ScrapeResult | JSONResponse:
    logger.info(f"Scrape request for: {request.url}")

    if request.callback_url:
        task = asyncio.create_task(
            _scrape_and_callback(scraper, request.url, request.callback_url, request.callback_secret)
        )
        _background_tasks.add(task)
        task.add_done_callback(_background_tasks.discard)
        return JSONResponse(
            status_code=202,
            content={"status": "accepted", "url": request.url},
        )

    return await scraper.scrape(request.url)


async def _scrape_and_callback(
    scraper: PlaywrightScraper,
    url: str,
    callback_url: str,
    callback_secret: str | None,
) -> None:
    logger.info(f"Starting async scrape for {url}, will callback to {callback_url}")
    try:
        result = await scraper.scrape(url)
        headers = {"Content-Type": "application/json"}
        if callback_secret:
            headers[CALLBACK_SECRET_HEADER] = callback_secret

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(
                callback_url,
                content=result.model_dump_json(),
                headers=headers,
            )
            response.raise_for_status()
            logger.info(f"Callback delivered to {callback_url}")
    except Exception as error:
        logger.error(
            f"Scrape or callback failed for {url} -> {callback_url}: {error}",
            exc_info=True,
        )
