from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str
    callback_url: str | None = None
    callback_secret: str | None = None


class ScrapeResult(BaseModel):
    text: str
    image_urls: list[str]
    video_urls: list[str]
    logo: str | None = None
    screenshot: str | None = None
    page_urls: list[str]
