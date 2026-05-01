from fastapi import Depends

from aimarketing.lib.scraper.model import ScrapeResult
from aimarketing.lib.scraper.playwright_scraper import PlaywrightScraper


class WebsiteScraperService:
    def __init__(self, scraper: PlaywrightScraper = Depends()):
        self.scraper = scraper

    async def scrape(self, url: str) -> ScrapeResult:
        return await self.scraper.scrape_async(url)
