from pydantic import BaseModel


class ScrapeResult(BaseModel):
    text: str
    image_urls: list[str]
    video_urls: list[str]
    logo: str | None = None
    screenshot: str | None = None  # Public URL to the screenshot in Supabase storage
    page_urls: list[str]
