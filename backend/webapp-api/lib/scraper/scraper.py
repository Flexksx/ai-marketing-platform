from abc import ABC, abstractmethod

from scraper_api_contract.scraper import ScrapeResult


class WebsiteScraper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> ScrapeResult:
        pass

    @abstractmethod
    async def scrape_async(self, url: str) -> ScrapeResult:
        pass

    @abstractmethod
    def get_text(self, url: str) -> str:
        pass

    @abstractmethod
    async def get_text_async(self, url: str) -> str:
        pass

    @abstractmethod
    def get_image_urls(self, url: str) -> list[str]:
        pass

    @abstractmethod
    async def get_image_urls_async(self, url: str) -> list[str]:
        pass

    @abstractmethod
    def get_video_urls(self, url: str) -> list[str]:
        pass

    @abstractmethod
    async def get_video_urls_async(self, url: str) -> list[str]:
        pass

    @abstractmethod
    def get_logo_url(self, url: str) -> str | None:
        pass

    @abstractmethod
    async def get_logo_url_async(self, url: str) -> str | None:
        pass

    @abstractmethod
    def get_screenshot(self, url: str) -> str | None:
        pass

    @abstractmethod
    async def get_screenshot_async(self, url: str) -> str | None:
        pass

    @abstractmethod
    def get_page_urls(self, url: str) -> list[str]:
        pass

    @abstractmethod
    async def get_page_urls_async(self, url: str) -> list[str]:
        pass
