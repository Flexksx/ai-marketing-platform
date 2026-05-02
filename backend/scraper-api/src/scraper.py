import logging
import shutil
import uuid
from urllib.parse import urljoin, urlparse

import html2text
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from scraper_api_contract.scraper import ScrapeResult
from src.storage import (
    StorageBucket,
    StorageUploadRequest,
    upload_public,
)


logger = logging.getLogger(__name__)


class PlaywrightScraper:
    def __init__(self) -> None:
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._html_converter = html2text.HTML2Text()
        self._html_converter.ignore_links = False
        self._html_converter.ignore_images = False
        self._html_converter.body_width = 0

    async def _ensure_browser(self) -> None:
        if self._context:
            return
        if not self._playwright:
            logger.debug("Starting Playwright")
            self._playwright = await async_playwright().start()
        if not self._browser:
            chromium_path = shutil.which("chromium") or shutil.which("chromium-browser")
            if chromium_path:
                logger.info(f"Launching Chromium from system path: {chromium_path}")
                self._browser = await self._playwright.chromium.launch(
                    headless=True, executable_path=chromium_path
                )
            else:
                logger.info("Launching Chromium using default Playwright browser")
                self._browser = await self._playwright.chromium.launch(headless=True)
        logger.debug("Creating browser context")
        self._context = await self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )

    async def _cleanup(self) -> None:
        if self._context:
            await self._context.close()
            self._context = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    async def __aenter__(self) -> PlaywrightScraper:
        await self._ensure_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._cleanup()

    async def scrape(self, url: str) -> ScrapeResult:
        logger.info(f"Starting scrape for URL: {url}")
        await self._ensure_browser()
        assert self._context is not None

        page = await self._context.new_page()
        try:
            await page.goto(url, wait_until="load", timeout=60000)

            html_content = await page.content()
            text = self._html_converter.handle(html_content)

            image_urls = await self._extract_image_urls(page, url)
            video_urls = await self._extract_video_urls(page, url)
            logo_url = await self._extract_logo_url(page, url)
            screenshot_url = await self._capture_screenshot(page)
            page_urls = await self._extract_page_urls(page, url)

            logger.info(
                f"Scrape completed for {url}: {len(text)} chars, "
                f"{len(image_urls)} images, {len(page_urls)} pages"
            )
            return ScrapeResult(
                text=text,
                image_urls=image_urls,
                video_urls=video_urls,
                logo=logo_url,
                screenshot=screenshot_url,
                page_urls=page_urls,
            )
        finally:
            await page.close()

    def _is_supported_image_format(self, url: str) -> bool:
        if not url:
            return False
        url_lower = url.lower()
        if ".svg" in url_lower:
            return False
        supported = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        return any(
            url_lower.endswith(ext) or f".{ext[1:]}" in url_lower for ext in supported
        )

    async def _extract_image_urls(self, page: Page, base_url: str) -> list[str]:
        image_elements = await page.query_selector_all("img")
        image_urls: list[str] = []

        for img in image_elements:
            src = await img.get_attribute("src")
            if not src or not self._is_supported_image_format(src):
                continue
            try:
                dims = await img.evaluate(
                    "(el) => ({ width: el.naturalWidth || el.width || 0, "
                    "height: el.naturalHeight || el.height || 0 })"
                )
                w, h = dims.get("width", 0), dims.get("height", 0)
            except Exception:
                try:
                    bb = await img.bounding_box()
                    w = bb.get("width", 0) if bb else 0
                    h = bb.get("height", 0) if bb else 0
                except Exception:
                    continue

            if w > 300 and h > 300:
                abs_url = self._resolve_url(base_url, src)
                if (
                    abs_url
                    and abs_url not in image_urls
                    and self._is_supported_image_format(abs_url)
                ):
                    image_urls.append(abs_url)

        return image_urls

    async def _extract_video_urls(self, page: Page, base_url: str) -> list[str]:
        video_urls: list[str] = []

        for video in await page.query_selector_all("video"):
            src = await video.get_attribute("src")
            if src:
                abs_url = self._resolve_url(base_url, src)
                if abs_url and abs_url not in video_urls:
                    video_urls.append(abs_url)

        for source in await page.query_selector_all("video > source"):
            src = await source.get_attribute("src")
            if src:
                abs_url = self._resolve_url(base_url, src)
                if abs_url and abs_url not in video_urls:
                    video_urls.append(abs_url)

        for iframe in await page.query_selector_all(
            "iframe[src*='youtube'], iframe[src*='vimeo']"
        ):
            src = await iframe.get_attribute("src")
            if src and src not in video_urls:
                video_urls.append(src)

        return video_urls

    async def _extract_logo_url(self, page: Page, base_url: str) -> str | None:
        selectors = [
            'img[alt*="logo" i]',
            'img[class*="logo" i]',
            'img[id*="logo" i]',
            'a[class*="logo" i] img',
            'header img[src*="logo" i]',
            'nav img[src*="logo" i]',
        ]
        for selector in selectors:
            el = await page.query_selector(selector)
            if el:
                src = await el.get_attribute("src")
                if src:
                    return self._resolve_url(base_url, src)
        return None

    async def _capture_screenshot(self, page: Page) -> str | None:
        try:
            viewport = page.viewport_size
            vh = viewport.get("height", 1080) if viewport else 1080
            vw = viewport.get("width", 1920) if viewport else 1920
            content_h = await page.evaluate(
                "() => document.documentElement.scrollHeight"
            )
            clip_h = min(content_h, vh * 2)

            screenshot_bytes = await page.screenshot(
                clip={"x": 0, "y": 0, "width": vw, "height": clip_h}
            )
            if not screenshot_bytes:
                return None

            path = f"screenshots/{uuid.uuid4().hex}.png"
            result = await upload_public(
                StorageUploadRequest(
                    bucket=StorageBucket.BRAND_EXTRACTION,
                    path=path,
                    content=screenshot_bytes,
                    content_type="image/png",
                )
            )
            return result.public_url if result else None
        except Exception as e:
            logger.warning(f"Screenshot capture failed (non-critical): {e}")
            return None

    async def _extract_page_urls(self, page: Page, base_url: str) -> list[str]:
        page_urls: list[str] = []
        for link in await page.query_selector_all("a[href]"):
            href = await link.get_attribute("href")
            if href:
                abs_url = self._resolve_url(base_url, href)
                if abs_url and abs_url.startswith("http") and abs_url not in page_urls:
                    page_urls.append(abs_url)
        return page_urls

    def _resolve_url(self, base_url: str, relative_url: str) -> str | None:
        if not relative_url:
            return None
        if relative_url.startswith(
            ("data:", "blob:", "javascript:", "mailto:", "tel:")
        ):
            return None
        if relative_url.startswith(("http://", "https://")):
            return relative_url
        try:
            resolved = urljoin(base_url, relative_url)
            parsed = urlparse(resolved)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                return resolved
        except Exception:
            pass
        return None
