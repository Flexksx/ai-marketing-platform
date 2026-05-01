import logging

import public
from fastapi import Depends
from pydantic import BaseModel
from pydantic_ai import ImageUrl

from services.worker_api.campaign_generation.content_brief.service import (
    CampaignContentBriefGenerator,
)
from aimarketing.domain.brand import Brand
from aimarketing.domain.brand.service import BrandService
from aimarketing.domain.campaign_generation import (
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from aimarketing.domain.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)
from aimarketing.domain.content_channel import ContentChannel, ContentChannelService
from aimarketing.lib.prompts import PromptService, PromptTemplateName


logger = logging.getLogger(__name__)


class _CampaignDescriptionDeps(BaseModel):
    brand: Brand
    content_channels: list[ContentChannel]
    user_input: UserMediaOnlyCampaignGenerationJobUserInput


@public.add
class UserMediaContentBriefGenerator:
    def __init__(
        self,
        brand_service: BrandService = Depends(),
        prompt_service: PromptService = Depends(),
        content_channel_service: ContentChannelService = Depends(),
        content_brief_generator: CampaignContentBriefGenerator = Depends(),
    ):
        self.brand_service = brand_service
        self.prompt_service = prompt_service
        self.content_channel_service = content_channel_service
        self.content_brief_generator = content_brief_generator

    async def generate(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        brand = await self.brand_service.get(job.brand_id)
        user_input = self.__get_user_input_or_raise(job)
        return await self.content_brief_generator.generate(
            job_id=job.id,
            brand_id=brand.id,
            user_prompt=user_input.prompt,
            image_urls=self.__get_user_image_urls(user_input),
            description_prompt_name=PromptTemplateName.CAMPAIGN_GENERATION_DESCRIPTION_STEP,
        )

    def __get_user_image_urls(
        self, user_input: UserMediaOnlyCampaignGenerationJobUserInput
    ) -> list[ImageUrl]:
        return [ImageUrl(url=image_url) for image_url in user_input.image_urls]

    def __get_user_input_or_raise(
        self, job: CampaignGenerationJob
    ) -> UserMediaOnlyCampaignGenerationJobUserInput:
        if not isinstance(job.user_input, UserMediaOnlyCampaignGenerationJobUserInput):
            logger.error(
                f"""Job {job.id} - expected UserMediaOnlyCampaignGenerationJobUserInput,
                got {type(job.user_input).__name__}.
                Job workflow_type: {job.workflow_type},
                user_input type: {type(job.user_input)},
                user_input value: {job.user_input}
                """
            )
            raise ValueError(f"User input is not a valid user input for job {job.id}")
        return job.user_input
