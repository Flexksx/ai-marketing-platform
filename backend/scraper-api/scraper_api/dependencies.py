from fastapi import Request

from scraper_api.scraper import PlaywrightScraper


def get_scraper(request: Request) -> PlaywrightScraper:
    return request.app.state.scraper
