import asyncio
import base64
import logging
import uuid
from collections.abc import Awaitable, Callable
from typing import TypeVar

import httpx
import public
from fastapi import Depends
from pydantic import BaseModel
from pydantic_ai import (
    Agent,
    ImageUrl,
    RunContext,
)

from services.worker_api.shared.text_with_single_image.model import (
    TextWithSingleImageContent,
)
from aimarketing.domain.brand import Brand, BrandService
from aimarketing.domain.content_channel import (
    ContentChannelName,
    ContentChannelService,
    ContentFormat,
)
from aimarketing.lib.ai_agents import PydanticAiModel
from aimarketing.lib.nano_banana import (
    NanoBananaRequest,
    NanoBananaResponse,
    NanoBananaService,
)
from aimarketing.lib.prompts import PromptService, PromptTemplateName
from aimarketing.lib.supabase_client import (
    StorageBucket,
    StorageUploadRequest,
    SupabaseStorageService,
)


logger = logging.getLogger(__name__)

T = TypeVar("T")


@public.add
class TextWithSingleImageAgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName
    user_prompt: str
    image_prompt_template_name: PromptTemplateName
    caption_prompt_template_name: PromptTemplateName


class CaptionAgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName
    user_prompt: str
    caption_prompt_template_name: PromptTemplateName


@public.add
class TextWithSingleImageContentGenerator:
    def __init__(
        self,
        brand_service: BrandService = Depends(),
        content_channel_service: ContentChannelService = Depends(),
        supabase_storage_service: SupabaseStorageService = Depends(),
        prompt_service: PromptService = Depends(),
        nano_banana_service: NanoBananaService = Depends(),
    ):
        self.brand_service = brand_service
        self.content_channel_service = content_channel_service
        self.supabase_storage_service = supabase_storage_service
        self.prompt_service = prompt_service
        self.nano_banana_service = nano_banana_service
        self.__caption_agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LATEST,
            deps_type=CaptionAgentDependencies,
            output_type=str,
        )

        @self.__caption_agent.system_prompt
        def _configure_caption_generation_system_prompt(
            context: RunContext[CaptionAgentDependencies],
        ):
            return self.prompt_service.render(
                context.deps.caption_prompt_template_name,
                context.deps.model_dump(),
            )

    async def generate_caption_for_image(
        self,
        brand_id: str,
        channel: ContentChannelName,
        caption_prompt_template_name: PromptTemplateName,
        user_prompt: str,
        image_url: str,
        max_retries: int = 3,
    ) -> str:
        return await self.__retry_with_backoff(
            operation=lambda: self.__generate_caption_for_image(
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

    async def generate_full(
        self,
        brand_id: str,
        channel: ContentChannelName,
        image_prompt_template_name: PromptTemplateName,
        caption_prompt_template_name: PromptTemplateName,
        user_prompt: str,
        image_url: str | None,
        max_retries: int = 3,
    ) -> TextWithSingleImageContent:
        return await self.__retry_with_backoff(
            operation=lambda: self.__generate_once(
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

    async def __generate_once(
        self,
        brand_id: str,
        channel: ContentChannelName,
        image_prompt_template_name: PromptTemplateName,
        caption_prompt_template_name: PromptTemplateName,
        user_prompt: str,
        image_url: str | None,
    ) -> TextWithSingleImageContent:
        brand = await self.brand_service.get(brand_id)
        deps = TextWithSingleImageAgentDependencies(
            brand=brand,
            channel=channel,
            user_prompt=user_prompt,
            image_prompt_template_name=image_prompt_template_name,
            caption_prompt_template_name=caption_prompt_template_name,
        )

        content_channel = self.content_channel_service.get(channel)
        image_urls_to_send: list[str] = []
        if image_url is not None:
            image_urls_to_send.append(image_url)
        image_result: NanoBananaResponse = await self.nano_banana_service.generate(
            NanoBananaRequest(
                image_urls=image_urls_to_send,
                aspect_ratio=content_channel.image_specification.aspect_ratio,
                image_size=content_channel.image_specification.resolution,
                prompt=self.prompt_service.render(
                    deps.image_prompt_template_name,
                    deps.model_dump(),
                ),
            )
        )

        generated_image_url = await self.__upload_generated_image(
            brand_id, image_result
        )
        caption_result = await self.__generate_caption_for_image(
            brand_id=brand_id,
            channel=channel,
            caption_prompt_template_name=caption_prompt_template_name,
            user_prompt=user_prompt,
            image_url=generated_image_url,
        )
        return TextWithSingleImageContent(
            text=caption_result,
            image_url=generated_image_url,
            channel=channel,
            content_type=ContentFormat.TEXT_WITH_SINGLE_IMAGE,
        )

    async def __retry_with_backoff(
        self,
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

    async def __generate_caption_for_image(
        self,
        brand_id: str,
        channel: ContentChannelName,
        caption_prompt_template_name: PromptTemplateName,
        user_prompt: str,
        image_url: str,
    ) -> str:
        brand = await self.brand_service.get(brand_id)
        deps = CaptionAgentDependencies(
            brand=brand,
            channel=channel,
            user_prompt=user_prompt,
            caption_prompt_template_name=caption_prompt_template_name,
        )
        caption_run_result = await self.__caption_agent.run(
            user_prompt=[user_prompt, ImageUrl(url=image_url)], deps=deps
        )
        return caption_run_result.output

    async def __upload_generated_image(
        self,
        brand_id: str,
        nano_banana_response: NanoBananaResponse,
    ) -> str:
        mime_type = nano_banana_response.mime_type
        image_data_base64 = nano_banana_response.image_data_base64
        extension = mime_type.split("/")[-1] if "/" in mime_type else "png"
        filename = f"{brand_id}/{uuid.uuid4().hex[:8]}.{extension}"
        image_bytes = base64.b64decode(image_data_base64)
        upload_request = StorageUploadRequest(
            bucket=StorageBucket.CONTENT_GENERATION_AI_IMAGES,
            path=filename,
            content=image_bytes,
            content_type=mime_type,
        )
        upload_result = await self.supabase_storage_service.upload_public(
            upload_request
        )
        return upload_result.public_url
