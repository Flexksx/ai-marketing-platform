from fastapi import Request

from src.scraper import PlaywrightScraper


def get_scraper(request: Request) -> PlaywrightScraper:
    return request.app.state.scraper
