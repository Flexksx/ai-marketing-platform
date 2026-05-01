from enum import StrEnum

import public


@public.add
class PydanticAiModel(StrEnum):
    GPT_5_MINI = "openai:gpt-5-mini"
    GPT_5_NANO = "openai:gpt-5-nano"
    GEMINI_2_5_FLASH = "google-gla:gemini-2.5-flash"
    GEMINI_2_5_FLASH_IMAGE = "google-gla:gemini-2.5-flash-image"
    GEMINI_FLASH_LATEST = "google-gla:gemini-flash-latest"
    GEMINI_FLASH_LITE_LATEST = "google-gla:gemini-flash-lite-latest"
