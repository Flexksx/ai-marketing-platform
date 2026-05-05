import logging

import html2text
import public
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from supabase import AsyncClient

import lib.supabase_client as supabase_storage
from lib.scraper.model import ScrapeResult
from lib.supabase_client import StorageBucket, StorageUploadRequest
from lib.utils import new_id


logger = logging.getLogger(__name__)


@public.add
class PlaywrightScraper:
    def __init__(self, supabase_client: AsyncClient):
        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._html_converter = html2text.HTML2Text()
        self._html_converter.ignore_links = False
        self._html_converter.ignore_images = False
        self._html_converter.body_width = 0
        self._supabase_client = supabase_client

    async def start(self) -> None:
        if self._context:
            return
        if not self._playwright:
            logger.debug("Starting Playwright")
            self._playwright = await async_playwright().start()
        if not self._browser:
            import shutil

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

    async def stop(self) -> None:
        if self._context:
            logger.debug("Closing browser context")
            await self._context.close()
            self._context = None
        if self._browser:
            logger.debug("Closing browser")
            await self._browser.close()
            self._browser = None
        if self._playwright:
            logger.debug("Stopping Playwright")
            await self._playwright.stop()
            self._playwright = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def scrape(self, url: str) -> ScrapeResult:
        logger.info(f"Starting scrape for URL: {url}")
        await self.start()
        assert self._context is not None

        page = await self._context.new_page()
        try:
            logger.debug(f"Navigating to {url}")
            await page.goto(url, wait_until="load", timeout=60000)
            logger.debug("Page loaded, extracting content")

            html_content = await page.content()
            text = self._html_converter.handle(html_content)
            logger.debug(f"Extracted text length: {len(text)} characters")

            logger.debug("Extracting images")
            image_urls = await self._extract_image_urls(page, url)
            logger.info(f"Found {len(image_urls)} images")

            logger.debug("Extracting videos")
            video_urls = await self._extract_video_urls(page, url)
            logger.info(f"Found {len(video_urls)} videos")

            logger.debug("Extracting logo")
            logo_url = await self._extract_logo_url(page, url)
            if logo_url:
                logger.info(f"Found logo: {logo_url}")

            logger.debug("Capturing screenshot")
            screenshot_url = await self._capture_screenshot(page)
            if screenshot_url:
                logger.debug(f"Screenshot uploaded: {screenshot_url}")

            logger.debug("Extracting page URLs")
            page_urls = await self._extract_page_urls(page, url)
            logger.info(f"Found {len(page_urls)} page URLs")

            result = ScrapeResult(
                text=text,
                image_urls=image_urls,
                video_urls=video_urls,
                logo=logo_url,
                screenshot=screenshot_url,
                page_urls=page_urls,
            )
            logger.info(f"Scrape completed successfully for {url}")
            return result
        except Exception as e:
            logger.error(f"Error scraping {url}: {e!s}", exc_info=True)
            raise
        finally:
            await page.close()

    def _is_supported_image_format(self, url: str) -> bool:
        if not url:
            return False

        url_lower = url.lower()
        supported_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        if any(url_lower.endswith(ext) for ext in supported_extensions):
            return True

        if any(
            f"/{ext[1:]}" in url_lower or f".{ext[1:]}" in url_lower
            for ext in supported_extensions
        ):
            return True

        if ".svg" in url_lower:
            return False

        return True

    async def _extract_image_urls(self, page: Page, base_url: str) -> list[str]:
        image_elements = await page.query_selector_all("img")
        logger.debug(f"Found {len(image_elements)} image elements")
        image_urls = []
        skipped_count = 0
        unsupported_format_count = 0

        for img in image_elements:
            src = await img.get_attribute("src")
            if not src:
                continue

            if not self._is_supported_image_format(src):
                unsupported_format_count += 1
                logger.debug(f"Skipping unsupported image format: {src}")
                continue

            try:
                dimensions = await img.evaluate(
                    """(element) => {
                        return {
                            width: element.naturalWidth || element.width || 0,
                            height: element.naturalHeight || element.height || 0
                        };
                    }"""
                )
                width = dimensions.get("width", 0)
                height = dimensions.get("height", 0)

                if width > 300 and height > 300:
                    absolute_url = self._resolve_url(base_url, src)
                    if absolute_url and absolute_url not in image_urls:
                        if self._is_supported_image_format(absolute_url):
                            image_urls.append(absolute_url)
                            logger.debug(
                                f"Added image: {absolute_url} ({width}x{height})"
                            )
                        else:
                            unsupported_format_count += 1
                            logger.debug(
                                f"Skipping unsupported format after URL resolution: {absolute_url}"
                            )
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                logger.debug(
                    f"Error evaluating image dimensions, trying bounding box: {e}"
                )
                try:
                    bounding_box = await img.bounding_box()
                    if bounding_box:
                        width = bounding_box.get("width", 0)
                        height = bounding_box.get("height", 0)
                        if width > 300 and height > 300:
                            absolute_url = self._resolve_url(base_url, src)
                            if absolute_url and absolute_url not in image_urls:
                                if self._is_supported_image_format(absolute_url):
                                    image_urls.append(absolute_url)
                                    logger.debug(
                                        f"Added image (via bounding box): {absolute_url} ({width}x{height})"
                                    )
                                else:
                                    unsupported_format_count += 1
                                    logger.debug(
                                        f"Skipping unsupported format after URL resolution: {absolute_url}"
                                    )
                            else:
                                skipped_count += 1
                        else:
                            skipped_count += 1
                except Exception as e2:
                    logger.debug(f"Error getting bounding box: {e2}")
                    skipped_count += 1

        if skipped_count > 0:
            logger.debug(f"Skipped {skipped_count} images (too small or invalid)")
        if unsupported_format_count > 0:
            logger.debug(
                f"Skipped {unsupported_format_count} images (unsupported format)"
            )
        return image_urls

    async def _extract_video_urls(self, page: Page, base_url: str) -> list[str]:
        video_urls = []

        video_elements = await page.query_selector_all("video")
        for video in video_elements:
            src = await video.get_attribute("src")
            if src:
                absolute_url = self._resolve_url(base_url, src)
                if absolute_url and absolute_url not in video_urls:
                    video_urls.append(absolute_url)

        source_elements = await page.query_selector_all("video > source")
        for source in source_elements:
            src = await source.get_attribute("src")
            if src:
                absolute_url = self._resolve_url(base_url, src)
                if absolute_url and absolute_url not in video_urls:
                    video_urls.append(absolute_url)

        iframe_elements = await page.query_selector_all(
            "iframe[src*='youtube'], iframe[src*='vimeo']"
        )
        for iframe in iframe_elements:
            src = await iframe.get_attribute("src")
            if src and src not in video_urls:
                video_urls.append(src)

        return video_urls

    async def _extract_logo_url(self, page: Page, base_url: str) -> str | None:
        logo_selectors = [
            'img[alt*="logo" i]',
            'img[class*="logo" i]',
            'img[id*="logo" i]',
            'a[class*="logo" i] img',
            'header img[src*="logo" i]',
            'nav img[src*="logo" i]',
        ]

        for selector in logo_selectors:
            element = await page.query_selector(selector)
            if element:
                src = await element.get_attribute("src")
                if src:
                    return self._resolve_url(base_url, src)

        return None

    async def _capture_screenshot(self, page: Page) -> str | None:
        try:
            viewport_size = page.viewport_size
            if not viewport_size:
                logger.warning("Could not get viewport size, using default")
                viewport_height = 1080
                viewport_width = 1920
            else:
                viewport_height = viewport_size.get("height", 1080)
                viewport_width = viewport_size.get("width", 1920)

            content_height = await page.evaluate(
                "() => document.documentElement.scrollHeight"
            )
            content_width = await page.evaluate(
                "() => document.documentElement.scrollWidth"
            )

            max_screenshot_height = min(content_height, viewport_height * 2)

            logger.debug(
                f"Screenshot dimensions: viewport={viewport_width}x{viewport_height}, "
                f"content={content_width}x{content_height}, "
                f"capturing={viewport_width}x{max_screenshot_height}"
            )

            screenshot_bytes = await page.screenshot(
                clip={
                    "x": 0,
                    "y": 0,
                    "width": viewport_width,
                    "height": max_screenshot_height,
                }
            )
            if not screenshot_bytes:
                logger.debug("Screenshot capture returned empty bytes")
                return None

            screenshot_id = new_id()
            screenshot_path = f"screenshots/{screenshot_id}.png"

            upload_request = StorageUploadRequest(
                bucket=StorageBucket.BRAND_EXTRACTION,
                path=screenshot_path,
                content=screenshot_bytes,
                content_type="image/png",
            )

            upload_result = await supabase_storage.upload_public(
                self._supabase_client, upload_request
            )
            logger.info(f"Screenshot uploaded to Supabase: {upload_result.public_url}")
            return upload_result.public_url
        except Exception as e:
            logger.warning(
                f"Failed to upload screenshot to Supabase storage (this is non-critical): {e}. "
                f"Brand extraction will continue without screenshot. "
                f"If this persists, ensure SUPABASE_SERVICE_ROLE_KEY is set in your environment."
            )
            return None

    async def _extract_page_urls(self, page: Page, base_url: str) -> list[str]:
        link_elements = await page.query_selector_all("a[href]")
        page_urls = []

        for link in link_elements:
            href = await link.get_attribute("href")
            if href:
                absolute_url = self._resolve_url(base_url, href)
                if (
                    absolute_url
                    and absolute_url.startswith("http")
                    and absolute_url not in page_urls
                ):
                    page_urls.append(absolute_url)

        return page_urls

    def _resolve_url(self, base_url: str, relative_url: str) -> str | None:
        from urllib.parse import urljoin, urlparse

        if not relative_url:
            return None

        if relative_url.startswith(
            ("data:", "blob:", "javascript:", "mailto:", "tel:")
        ):
            return None

        if relative_url.startswith("http://") or relative_url.startswith("https://"):
            return relative_url

        try:
            resolved = urljoin(base_url, relative_url)
            parsed = urlparse(resolved)
            if parsed.scheme and parsed.netloc and parsed.scheme in ("http", "https"):
                return resolved
        except Exception:
            pass

        return None
