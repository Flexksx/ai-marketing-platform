from functools import lru_cache

import httpx
from google import genai

from src.config import get_settings


@lru_cache
def get_genai_client() -> genai.Client:
    settings = get_settings()
    api_key = settings.gemini_api_key

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    return genai.Client(
        api_key=api_key,
        vertexai=False,
    )


@lru_cache
def get_http_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=60.0)
