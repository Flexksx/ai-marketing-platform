import logging

from pydantic_ai import ImageUrl

from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.campaign_generation.generation.content_brief.service import (
    generate_campaign_content_brief,
)
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    UserMediaOnlyCampaignGenerationJobUserInput,
)


logger = logging.getLogger(__name__)


async def generate_content_brief(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
) -> CampaignGenerationJobResult:
    user_input = _get_user_input_or_raise(job)
    return await generate_campaign_content_brief(
        session_factory=session_factory,
        job_id=job.id,
        brand_id=job.brand_id,
        user_prompt=user_input.prompt,
        image_urls=[ImageUrl(url=url) for url in user_input.image_urls],
        description_prompt_name=PromptTemplateName.CAMPAIGN_GENERATION_DESCRIPTION_STEP,
    )


def _get_user_input_or_raise(
    job: CampaignGenerationJob,
) -> UserMediaOnlyCampaignGenerationJobUserInput:
    if not isinstance(job.user_input, UserMediaOnlyCampaignGenerationJobUserInput):
        logger.error(
            f"Job {job.id} - expected UserMediaOnlyCampaignGenerationJobUserInput, "
            f"got {type(job.user_input).__name__}. "
            f"workflow_type: {job.workflow_type}"
        )
        raise ValueError(f"User input is not a valid user input for job {job.id}")
    return job.user_input
