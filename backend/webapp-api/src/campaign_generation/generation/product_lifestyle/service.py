import logging

import public
from fastapi import Depends

from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.campaign_generation.generation.content_brief.ai_generated import (
    AIGeneratedContentBriefGenerator,
)
from src.campaign_generation.generation.content_generation.product_lifestyle import (
    ProductLifestyleContentPlanItemGenerator,
)
from src.campaign_generation.generation.content_plan import (
    AIGeneratedContentPlanGenerator,
)
from src.campaign_generation.generation.shared.service import (
    BaseCampaignGenerationJobRunner,
)
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)


logger = logging.getLogger(__name__)


@public.add
class ProductLifestyleCampaignGenerationJobRunner(BaseCampaignGenerationJobRunner):
    def __init__(
        self,
        session_factory: DbSessionFactory = Depends(),
        content_brief: AIGeneratedContentBriefGenerator = Depends(),
        content_plan: AIGeneratedContentPlanGenerator = Depends(),
        post_generation_step: ProductLifestyleContentPlanItemGenerator = Depends(),
    ):
        super().__init__(session_factory)
        self.content_brief = content_brief
        self.content_plan = content_plan
        self.post_generation_step = post_generation_step

    async def generate_content_brief(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing campaign content brief for job {job.id}")
        return await self.content_brief.generate(job)

    async def process_posting_plan(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing content plan for job {job.id}")
        return await self.content_plan.generate(
            job, PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP
        )

    async def process_post_generation(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing product lifestyle post generation for job {job.id}")
        return await self.post_generation_step.generate(job)
