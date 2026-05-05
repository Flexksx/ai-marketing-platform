import base64
import logging

import httpx
from google import genai
from google.genai import types

from lib.nano_banana.dependencies import get_genai_client, get_http_client
from lib.nano_banana.model import NanoBananaRequest, NanoBananaResponse


logger = logging.getLogger(__name__)

_MODEL = "gemini-2.5-flash-image"

_SAFETY_SETTINGS = [
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


async def generate(request: NanoBananaRequest) -> NanoBananaResponse:
    logger.info("Starting image generation with Nano Banana")
    http_client = get_http_client()
    parts = [await _fetch_as_image_part(url, http_client) for url in request.image_urls]
    parts.append(types.Part.from_text(text=request.prompt))
    contents = [types.Content(role="user", parts=parts)]
    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        response_modalities=["IMAGE"],
        safety_settings=_SAFETY_SETTINGS,
        image_config=types.ImageConfig(aspect_ratio=request.aspect_ratio),
    )
    response = await get_genai_client().aio.models.generate_content(
        model=_MODEL,
        contents=contents,  # pyright: ignore[reportArgumentType]  # ty:ignore[invalid-argument-type]
        config=config,
    )
    return _extract_image_response(response)


async def _fetch_as_image_part(url: str, http_client: httpx.AsyncClient) -> types.Part:
    image_bytes = await _fetch_image_bytes(url, http_client)
    return types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")


async def _fetch_image_bytes(url: str, http_client: httpx.AsyncClient) -> bytes:
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"URL must start with http:// or https://. Received: {url}")
    response = await http_client.get(url)
    response.raise_for_status()
    return response.content


def _extract_image_response(response) -> NanoBananaResponse:
    for part in response.parts or []:
        if part.inline_data:
            mime_type = part.inline_data.mime_type or "image/png"
            image_base64 = base64.b64encode(part.inline_data.data).decode("utf-8")
            return NanoBananaResponse(
                image_data_base64=image_base64, mime_type=mime_type
            )
    raise ValueError(f"Could not extract image data from response: {response}")
