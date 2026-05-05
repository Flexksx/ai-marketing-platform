from fastapi import Request

from lib.scraper.playwright_scraper import PlaywrightScraper


def get_playwright_scraper(request: Request) -> PlaywrightScraper:
    return request.app.state.playwright_scraper
