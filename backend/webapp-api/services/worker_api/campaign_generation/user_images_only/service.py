import logging

import public
from fastapi import Depends

from db.session_factory import DbSessionFactory
from services.worker_api.campaign_generation.content_brief.from_user_media import (
    UserMediaContentBriefGenerator,
)
from services.worker_api.campaign_generation.content_generation.from_user_media import (
    UserImagesOnlyPostGenerationCampaignGenerationStep,
)
from services.worker_api.campaign_generation.content_plan import (
    UserMediaContentPlanGenerator,
)
from services.worker_api.campaign_generation.shared.service import (
    BaseCampaignGenerationJobRunner,
)
from vozai.domain.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)


logger = logging.getLogger(__name__)


@public.add
class UserImagesOnlyCampaignGenerationJobRunner(BaseCampaignGenerationJobRunner):
    def __init__(
        self,
        session_factory: DbSessionFactory = Depends(),
        content_brief: UserMediaContentBriefGenerator = Depends(),
        content_plan: UserMediaContentPlanGenerator = Depends(),
        post_generation_step: UserImagesOnlyPostGenerationCampaignGenerationStep = Depends(),
    ):
        super().__init__(session_factory)
        self.content_brief = content_brief
        self.content_plan = content_plan
        self.post_generation_step = post_generation_step

    async def generate_content_brief(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing campaign description for job {job.id}")
        return await self.content_brief.generate(job)

    async def process_posting_plan(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing posting plan for job {job.id}")
        return await self.content_plan.generate(job)

    async def process_post_generation(
        self, job: CampaignGenerationJob
    ) -> CampaignGenerationJobResult:
        logger.info(f"Processing post generation for job {job.id}")
        return await self.post_generation_step.generate(job)
