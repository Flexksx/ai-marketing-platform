import asyncio
import logging
from urllib.parse import urlparse

import httpx
from fastapi import Depends
from scraper_api_contract.scraper import ScrapeResult

from lib.scraper.http_client import HttpScraperClient
from src.brand_generation_job.generation.steps.base import BrandGenerationBaseStep
from webapp_api_contract.brand_generation_job import (
    BrandGenerationJob,
    BrandGenerationResult,
)


logger = logging.getLogger(__name__)


class BrandScrapingStep(BrandGenerationBaseStep):
    def __init__(self, scraper: HttpScraperClient = Depends()):
        self.scraper = scraper

    async def _validate_url_accessible(
        self,
        url: str,
        job_id: str,
        max_retries: int = 5,
        delay_seconds: int = 2,
    ) -> bool:
        head_method_not_allowed_codes = (403, 405, 501)

        async with httpx.AsyncClient(timeout=10.0) as client:
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(
                        f"Validating URL accessibility "
                        f"(attempt {attempt}/{max_retries}): {url}",
                        extra={"job_id": job_id},
                    )
                    response = await client.head(url, follow_redirects=True)
                    if response.is_success:
                        logger.info(
                            f"URL is accessible: {url}",
                            extra={"job_id": job_id},
                        )
                        return True
                    if response.status_code in head_method_not_allowed_codes:
                        logger.info(
                            f"HEAD not allowed (status {response.status_code}), "
                            f"trying lightweight GET: {url}",
                            extra={"job_id": job_id},
                        )
                        get_response = await client.get(
                            url,
                            follow_redirects=True,
                            headers={"Range": "bytes=0-0"},
                        )
                        if get_response.is_success:
                            logger.info(
                                f"URL is accessible via GET: {url}",
                                extra={"job_id": job_id},
                            )
                            return True
                    logger.warning(
                        f"URL returned status {response.status_code} "
                        f"on attempt {attempt}: {url}",
                        extra={"job_id": job_id},
                    )
                except Exception as e:
                    logger.warning(
                        f"Failed to validate URL "
                        f"on attempt {attempt}/{max_retries}: {url}. "
                        f"Error: {e!s}",
                        extra={"job_id": job_id},
                    )

                if attempt < max_retries:
                    logger.info(
                        f"Waiting {delay_seconds}s before retry...",
                        extra={"job_id": job_id},
                    )
                    await asyncio.sleep(delay_seconds)

        logger.error(
            f"URL is not accessible after {max_retries} attempts: {url}",
            extra={"job_id": job_id},
        )
        return False

    def _find_about_url(self, base_url: str, page_urls: list[str]) -> str | None:
        base_domain = urlparse(base_url).netloc
        for url in page_urls:
            parsed = urlparse(url)
            if parsed.netloc == base_domain and "about" in parsed.path.lower():
                return url
        return None

    def _merge_scrape_results(
        self, main: ScrapeResult, about: ScrapeResult
    ) -> ScrapeResult:
        combined_text = main.text + "\n\n--- About Us Page ---\n\n" + about.text

        image_urls = list(dict.fromkeys(main.image_urls + about.image_urls))
        video_urls = list(dict.fromkeys(main.video_urls + about.video_urls))
        page_urls = list(dict.fromkeys(main.page_urls + about.page_urls))

        logo = main.logo or about.logo

        return ScrapeResult(
            text=combined_text,
            image_urls=image_urls,
            video_urls=video_urls,
            logo=logo,
            screenshot=main.screenshot,
            page_urls=page_urls,
        )

    async def execute(self, job: BrandGenerationJob) -> BrandGenerationResult:
        logger.info(
            f"Starting scraping step for job {job.id}, URL: {job.website_url}",
            extra={"job_id": job.id},
        )
        try:
            scrape_result = await self.scraper.scrape_async(job.website_url)
            text_len = len(scrape_result.text)
            image_count = len(scrape_result.image_urls)
            video_count = len(scrape_result.video_urls)
            page_count = len(scrape_result.page_urls)
            logger.info(
                f"Scraper completed for job {job.id}: "
                f"{text_len} chars, {image_count} images, "
                f"{video_count} videos, {page_count} pages",
                extra={"job_id": job.id},
            )

            if scrape_result.screenshot:
                logger.info(
                    f"Validating screenshot URL accessibility for job {job.id}: "
                    f"{scrape_result.screenshot}",
                    extra={"job_id": job.id},
                )
                is_accessible = await self._validate_url_accessible(
                    scrape_result.screenshot,
                    job.id,
                )
                if not is_accessible:
                    raise RuntimeError(
                        f"Screenshot URL is not accessible after retries: "
                        f"{scrape_result.screenshot}"
                    )

            about_url = self._find_about_url(job.website_url, scrape_result.page_urls)
            if about_url:
                logger.info(
                    f"Found about page URL for job {job.id}: {about_url}",
                    extra={"job_id": job.id},
                )
                try:
                    about_scrape_result = await self.scraper.scrape_async(about_url)
                    logger.info(
                        f"About page scraped successfully for job {job.id}: "
                        f"{len(about_scrape_result.text)} chars",
                        extra={"job_id": job.id},
                    )
                    scrape_result = self._merge_scrape_results(
                        scrape_result, about_scrape_result
                    )
                    logger.info(
                        f"Merged results for job {job.id}: "
                        f"{len(scrape_result.text)} chars total, "
                        f"{len(scrape_result.image_urls)} images, "
                        f"{len(scrape_result.video_urls)} videos",
                        extra={"job_id": job.id},
                    )
                except Exception as e:
                    logger.warning(
                        f"Failed to scrape about page for job {job.id}, "
                        f"URL {about_url}: {e!s}. "
                        f"Continuing with main page result only.",
                        exc_info=True,
                        extra={"job_id": job.id},
                    )
            else:
                logger.info(
                    f"No about page URL found for job {job.id}",
                    extra={"job_id": job.id},
                )

        except Exception as e:
            logger.error(
                f"Scraper failed for job {job.id}, URL {job.website_url}: {e!s}",
                exc_info=True,
                extra={"job_id": job.id},
            )
            raise

        current_result = job.result
        if not current_result:
            return BrandGenerationResult(
                scraper_result=scrape_result,
                brand_data=None,
            )
        return BrandGenerationResult(
            scraper_result=scrape_result,
            brand_data=None,
        )
