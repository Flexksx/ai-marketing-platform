import logging

import public
from fastapi import Depends

from services.worker_api.campaign_generation.content_brief import (
    AIGeneratedContentBriefGenerator,
)
from services.worker_api.campaign_generation.content_generation.ai_generated import (
    AIGeneratedCampaignContentGenerator,
)
from services.worker_api.campaign_generation.content_plan.ai_generated import (
    AIGeneratedContentPlanGenerator,
)
from services.worker_api.campaign_generation.shared.service import (
    BaseCampaignGenerationJobRunner,
)
from vozai.domain.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)
from vozai.domain.campaign_generation.service import CampaignGenerationJobService
from vozai.lib.prompts import PromptTemplateName


logger = logging.getLogger(__name__)


@public.add
class AIGeneratedCampaignGenerationJobRunner(BaseCampaignGenerationJobRunner):
    def __init__(
        self,
        campaign_generation_job_service: CampaignGenerationJobService = Depends(),
        content_brief: AIGeneratedContentBriefGenerator = Depends(),
        content_plan_generator: AIGeneratedContentPlanGenerator = Depends(),
        post_generation_step: AIGeneratedCampaignContentGenerator = Depends(),
    ):
        super().__init__(campaign_generation_job_service)
        self.content_brief = content_brief
        self.content_plan_generator = content_plan_generator
        self.campaign_content_generator = post_generation_step

    async def generate_content_brief(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Start processing campaign description for job {job.id}")
        return await self.content_brief.generate(job)

    async def process_posting_plan(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing posting plan for job {job.id}")
        return await self.content_plan_generator.generate(
            job, PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP
        )

    async def process_post_generation(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing AI-generated post generation for job {job.id}")
        return await self.campaign_content_generator.generate(job)
