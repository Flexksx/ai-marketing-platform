import logging

import public
from fastapi import Depends
from pydantic import BaseModel
from pydantic_ai import ImageUrl

import src.brand.service as brand_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.campaign_generation.generation.content_brief.service import (
    CampaignContentBriefGenerator,
)
from webapp_api_contract.brand import Brand
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from webapp_api_contract.shared import ContentChannel


logger = logging.getLogger(__name__)


class _CampaignDescriptionDeps(BaseModel):
    brand: Brand
    content_channels: list[ContentChannel]
    user_input: UserMediaOnlyCampaignGenerationJobUserInput


@public.add
class UserMediaContentBriefGenerator:
    def __init__(
        self,
        session_factory: DbSessionFactory = Depends(),
        prompt_service: PromptService = Depends(),
        content_brief_generator: CampaignContentBriefGenerator = Depends(),
    ):
        self.session_factory = session_factory
        self.prompt_service = prompt_service
        self.content_brief_generator = content_brief_generator

    async def generate(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        brand = await brand_service.get(self.session_factory, job.brand_id)
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
