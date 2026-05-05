import asyncio
import base64
import logging
import uuid
from collections.abc import Awaitable, Callable

import httpx
import public
from pydantic import BaseModel
from pydantic_ai import Agent, ImageUrl, RunContext

import lib.supabase_client.service as supabase_client_service
import src.brand.service as brand_service
import src.content_channel.service as content_channel_service
from lib import nano_banana, prompts
from lib.ai_agents import PydanticAiModel
from lib.model import ContentChannelName, ContentFormat
from lib.nano_banana import NanoBananaRequest, NanoBananaResponse
from lib.prompts import PromptTemplateName
from lib.supabase_client import StorageBucket, StorageUploadRequest
from src.auth import get_async_supabase_service_client
from src.brand.model import Brand


logger = logging.getLogger(__name__)


@public.add
class TextWithSingleImageContent(BaseModel):
    text: str
    image_url: str
    channel: ContentChannelName
    content_type: ContentFormat


class _ImageGenerationContext(BaseModel):
    brand: Brand
    channel: ContentChannelName
    user_prompt: str
    image_prompt_template_name: PromptTemplateName
    caption_prompt_template_name: PromptTemplateName


class _CaptionAgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName
    user_prompt: str
    caption_prompt_template_name: PromptTemplateName


_caption_agent: Agent[_CaptionAgentDependencies, str] = Agent(
    model=PydanticAiModel.GEMINI_FLASH_LATEST,
    deps_type=_CaptionAgentDependencies,
    output_type=str,
)


@_caption_agent.system_prompt
def _get_caption_system_prompt(context: RunContext[_CaptionAgentDependencies]) -> str:
    return prompts.render(
        context.deps.caption_prompt_template_name,
        context.deps.model_dump(),
    )


@public.add
async def generate_full(
    *,
    brand_id: str,
    channel: ContentChannelName,
    image_prompt_template_name: PromptTemplateName,
    caption_prompt_template_name: PromptTemplateName,
    user_prompt: str,
    image_url: str | None,
    max_retries: int = 3,
) -> TextWithSingleImageContent:
    return await _retry_with_backoff(
        operation=lambda: _generate_full_once(
            brand_id=brand_id,
            channel=channel,
            image_prompt_template_name=image_prompt_template_name,
            caption_prompt_template_name=caption_prompt_template_name,
            user_prompt=user_prompt,
            image_url=image_url,
        ),
        operation_name="text_with_single_image generation",
        brand_id=brand_id,
        channel=channel,
        max_retries=max_retries,
    )


@public.add
async def generate_caption_for_image(
    *,
    brand_id: str,
    channel: ContentChannelName,
    caption_prompt_template_name: PromptTemplateName,
    user_prompt: str,
    image_url: str,
    max_retries: int = 3,
) -> str:
    return await _retry_with_backoff(
        operation=lambda: _generate_caption(
            brand_id=brand_id,
            channel=channel,
            caption_prompt_template_name=caption_prompt_template_name,
            user_prompt=user_prompt,
            image_url=image_url,
        ),
        operation_name="caption generation",
        brand_id=brand_id,
        channel=channel,
        max_retries=max_retries,
    )


async def _generate_full_once(
    *,
    brand_id: str,
    channel: ContentChannelName,
    image_prompt_template_name: PromptTemplateName,
    caption_prompt_template_name: PromptTemplateName,
    user_prompt: str,
    image_url: str | None,
) -> TextWithSingleImageContent:
    brand = await brand_service.get(brand_id)
    context = _ImageGenerationContext(
        brand=brand,
        channel=channel,
        user_prompt=user_prompt,
        image_prompt_template_name=image_prompt_template_name,
        caption_prompt_template_name=caption_prompt_template_name,
    )
    content_channel = content_channel_service.get(channel)
    image_urls_to_send = [image_url] if image_url is not None else []
    image_result: NanoBananaResponse = await nano_banana.generate(
        NanoBananaRequest(
            image_urls=image_urls_to_send,
            aspect_ratio=content_channel.image_specification.aspect_ratio,
            image_size=content_channel.image_specification.resolution,
            prompt=prompts.render(image_prompt_template_name, context.model_dump()),
        ),
    )
    generated_image_url = await _upload_image(
        brand_id=brand_id,
        nano_banana_response=image_result,
    )
    caption = await _generate_caption(
        brand_id=brand_id,
        channel=channel,
        caption_prompt_template_name=caption_prompt_template_name,
        user_prompt=user_prompt,
        image_url=generated_image_url,
    )
    return TextWithSingleImageContent(
        text=caption,
        image_url=generated_image_url,
        channel=channel,
        content_type=ContentFormat.TEXT_WITH_SINGLE_IMAGE,
    )


async def _generate_caption(
    *,
    brand_id: str,
    channel: ContentChannelName,
    caption_prompt_template_name: PromptTemplateName,
    user_prompt: str,
    image_url: str,
) -> str:
    brand = await brand_service.get(brand_id)
    deps = _CaptionAgentDependencies(
        brand=brand,
        channel=channel,
        user_prompt=user_prompt,
        caption_prompt_template_name=caption_prompt_template_name,
    )
    result = await _caption_agent.run(
        user_prompt=[user_prompt, ImageUrl(url=image_url)],
        deps=deps,
    )
    return result.output


async def _upload_image(
    *,
    brand_id: str,
    nano_banana_response: NanoBananaResponse,
) -> str:
    mime_type = nano_banana_response.mime_type
    extension = mime_type.split("/")[-1] if "/" in mime_type else "png"
    filename = f"{brand_id}/{uuid.uuid4().hex[:8]}.{extension}"
    image_bytes = base64.b64decode(nano_banana_response.image_data_base64)
    supabase_client = await get_async_supabase_service_client()
    upload_result = await supabase_client_service.upload_public(
        supabase_client,
        StorageUploadRequest(
            bucket=StorageBucket.CONTENT_GENERATION_AI_IMAGES,
            path=filename,
            content=image_bytes,
            content_type=mime_type,
        ),
    )
    return upload_result.public_url


async def _retry_with_backoff[T](
    operation: Callable[[], Awaitable[T]],
    operation_name: str,
    brand_id: str,
    channel: ContentChannelName,
    max_retries: int,
) -> T:
    base_delay = 1.0

    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as exception:
            is_retryable = isinstance(exception, httpx.ReadError) or (
                isinstance(exception, OSError)
                and getattr(exception, "errno", None) in {11}
            )

            if not is_retryable:
                logger.error(
                    f"{operation_name} failed (non-retryable)",
                    extra={
                        "brand_id": brand_id,
                        "channel": str(channel),
                        "error_type": type(exception).__name__,
                    },
                    exc_info=exception,
                )
                raise

            error_type = type(exception).__name__
            errno = getattr(exception, "errno", None)

            if attempt == max_retries - 1:
                logger.error(
                    f"{operation_name} failed after retries",
                    extra={
                        "brand_id": brand_id,
                        "channel": str(channel),
                        "error_type": error_type,
                        "errno": errno,
                        "attempt": attempt + 1,
                        "max_retries": max_retries,
                    },
                    exc_info=exception,
                )
                raise

            sleep_seconds = base_delay * 2**attempt
            logger.warning(
                f"{operation_name} failed, retrying",
                extra={
                    "brand_id": brand_id,
                    "channel": str(channel),
                    "error_type": error_type,
                    "errno": errno,
                    "attempt": attempt + 1,
                    "max_retries": max_retries,
                    "sleep_seconds": sleep_seconds,
                },
            )
            await asyncio.sleep(sleep_seconds)

    raise RuntimeError(f"{operation_name} retries exhausted")
