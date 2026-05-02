from fastapi import Depends
from pydantic import BaseModel

from src.content_generation_job.generation.text_with_single_image.base_strategy import (
    BaseTextWithSingleImageContentGenerationJobStrategy,
)
from src.shared import (
    TextWithSingleImageContent,
    TextWithSingleImageContentGenerator,
)
from webapp_api_contract.brands import Brand
from webapp_api_contract.content import TextWithSingleImageContentData
from webapp_api_contract.shared import (
    ContentChannelName,
)
from webapp_api_contract.content_generation import (
    ContentGenerationJob,
    ContentGenerationJobInvalidUserInputException,
    ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
    TextWithSingleImageContentGenerationJobResult,
)
from lib.prompts import PromptTemplateName


class _AgentDependencies(BaseModel):
    brand: Brand
    channel: ContentChannelName


class ProductLifestyleTextWithSingleImageContentGenerationJobStrategy(
    BaseTextWithSingleImageContentGenerationJobStrategy
):
    def __init__(
        self,
        text_with_single_image_content_generation_service: TextWithSingleImageContentGenerator = Depends(),
    ):
        self.text_with_single_image_content_generation_service = (
            text_with_single_image_content_generation_service
        )

    async def generate(
        self, job: ContentGenerationJob
    ) -> TextWithSingleImageContentGenerationJobResult:
        user_input = self.__get_product_lifestyle_user_input_or_raise(job)
        result: TextWithSingleImageContent = await self.text_with_single_image_content_generation_service.generate_full(
            brand_id=job.brand_id,
            image_url=user_input.image_url,
            image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE_IMAGE,
            caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
            channel=user_input.channel,
            user_prompt=user_input.prompt,
        )

        return TextWithSingleImageContentGenerationJobResult(
            data=TextWithSingleImageContentData(
                image_url=result.image_url,
                caption=result.text,
            ),
            channel=result.channel,
            scheduled_at=user_input.scheduled_at,
        )

    def __get_product_lifestyle_user_input_or_raise(
        self, job: ContentGenerationJob
    ) -> ProductLifestyleTextWithSingleImageContentGenerationJobUserInput:
        if not isinstance(
            job.user_input,
            ProductLifestyleTextWithSingleImageContentGenerationJobUserInput,
        ):
            raise ContentGenerationJobInvalidUserInputException(
                job.id,
                "User input type is not valid for product lifestyle content generation job.",
            )
        return job.user_input
