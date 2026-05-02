import public
from fastapi import Depends

from lib.prompts import PromptTemplateName
from src.campaign_generation.generation.content_brief.service import (
    CampaignContentBriefGenerator,
)
from src.campaign_generation.model import CampaignGenerationJob
from webapp_api_contract.campaign_generation import (
    AiGeneratedCampaignGenerationJobUserInput,
    BaseCampaignGenerationJobUserInput,
    CampaignGenerationJobResult,
    ProductLifestyleCampaignGenerationJobUserInput,
)


@public.add
class AIGeneratedContentBriefGenerator:
    def __init__(
        self,
        content_brief_generator: CampaignContentBriefGenerator = Depends(),
    ):
        self.content_brief_generator = content_brief_generator

    async def generate(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        user_input = self.__get_user_input_or_raise(job)
        user_prompt = user_input.prompt
        return await self.content_brief_generator.generate(
            job_id=job.id,
            brand_id=job.brand_id,
            user_prompt=user_prompt,
            image_urls=[],
            description_prompt_name=PromptTemplateName.CAMPAIGN_GENERATION_DESCRIPTION_STEP,
        )

    def __get_user_input_or_raise(
        self, job: CampaignGenerationJob
    ) -> BaseCampaignGenerationJobUserInput:
        if not isinstance(
            job.user_input,
            (
                AiGeneratedCampaignGenerationJobUserInput,
                ProductLifestyleCampaignGenerationJobUserInput,
            ),
        ):
            raise ValueError(f"User input is not a valid user input for job {job.id}")
        return job.user_input
