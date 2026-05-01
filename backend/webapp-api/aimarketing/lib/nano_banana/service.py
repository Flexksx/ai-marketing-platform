import base64
import logging

import httpx
import public
from fastapi import Depends
from google import genai
from google.genai import types

from aimarketing.lib.nano_banana.dependencies import get_genai_client
from aimarketing.lib.nano_banana.schema import NanoBananaRequest, NanoBananaResponse


logger = logging.getLogger(__name__)

IMAGE_SIZE_TO_RESOLUTION: dict[str, str] = {
    "1K": "1024x1024",
    "2K": "2048x2048",
    "512": "512x512",
}


@public.add
class NanoBananaService:
    def __init__(self, client: genai.Client = Depends(get_genai_client)):
        self.client = client.aio
        self.model = "gemini-2.5-flash-image"
        self._http_client: httpx.AsyncClient | None = None

    async def _get_http_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=60.0)
        return self._http_client

    async def generate(self, request: NanoBananaRequest) -> NanoBananaResponse:
        try:
            logger.info("Starting image generation with Nano Banana Service")
            parts = []
            for url in request.image_urls:
                image_bytes = await self._fetch_image_bytes(url)
                parts.append(
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                )
            parts.append(types.Part.from_text(text=request.prompt))
            contents = [types.Content(role="user", parts=parts)]
            generate_content_config = types.GenerateContentConfig(
                temperature=1,
                top_p=0.95,
                response_modalities=["IMAGE"],
                safety_settings=self._get_safety_settings(),
                image_config=types.ImageConfig(
                    aspect_ratio=request.aspect_ratio,
                ),
            )
            response = await self.client.models.generate_content(
                model=self.model,
                contents=contents,  # pyright: ignore[reportArgumentType]  # ty:ignore[invalid-argument-type]
                config=generate_content_config,
            )

            return self._extract_image_response(response)

        except Exception as e:
            logger.error(f"Error in Nano Banana generation: {e}")
            raise

    async def _fetch_image_bytes(self, url: str) -> bytes:
        client = await self._get_http_client()
        response = await client.get(url)
        response.raise_for_status()
        return response.content

    def _get_safety_settings(self) -> list[types.SafetySetting]:
        return [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.OFF,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]

    async def _fetch_image_bytes(self, url: str) -> bytes:
        if not url or not url.startswith(("http://", "https://")):
            logger.error(f"NanoBananaService received an invalid URL: '{url}'")
            raise ValueError(
                f"URL must start with http:// or https://. Received: {url}"
            )

        client = await self._get_http_client()
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to fetch image from {url}: {e.response.status_code}")
            raise

    def _extract_image_response(self, response) -> NanoBananaResponse:
        image_bytes = None
        mime_type = "image/png"

        if hasattr(response, "parts") and response.parts:
            for part in response.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    if part.inline_data.mime_type:
                        mime_type = part.inline_data.mime_type
                    break

        if image_bytes is None:
            raise ValueError(f"Could not extract image data from response: {response}")

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        return NanoBananaResponse(image_data_base64=image_base64, mime_type=mime_type)
