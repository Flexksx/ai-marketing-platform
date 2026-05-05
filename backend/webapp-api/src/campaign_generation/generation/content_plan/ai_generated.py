import logging
from datetime import UTC

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, format_as_xml

import src.brand.service as brand_service
import src.content_channel.service as content_channel_service
import src.content_plan_item.service as content_plan_item_service
from lib.ai_agents import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.brand.model import Brand
from src.campaign_generation.errors import (
    CampaignGenerationJobResultNotFoundException,
)
from src.campaign_generation.generation.content_plan.model import (
    AgentGeneratedPostingPlanResult,
)
from src.campaign_generation.generation.errors import (
    CampaignGenerationJobGenerationFailureException,
)
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
)
from src.content_plan_item.model import ContentPlanItemCreateRequest
from src.shared.model import ContentChannel


logger = logging.getLogger(__name__)


class _AgentDependencies(BaseModel):
    brand: Brand
    available_channels: list[ContentChannel]
    prompt_template_name: PromptTemplateName


_prompt_service = PromptService()

_agent: Agent[_AgentDependencies, AgentGeneratedPostingPlanResult] = Agent(
    model=PydanticAiModel.GEMINI_FLASH_LATEST,
    deps_type=_AgentDependencies,
    output_type=AgentGeneratedPostingPlanResult,
)


@_agent.system_prompt
def _get_system_prompt(context: RunContext[_AgentDependencies]) -> str:
    return _prompt_service.render(
        context.deps.prompt_template_name,
        context.deps.model_dump(),
    )


async def generate_content_plan(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
    prompt_template_name: PromptTemplateName,
) -> CampaignGenerationJobResult:
    try:
        brand = await brand_service.get(session_factory, job.brand_id)
        campaign_description_result = job.result.content_brief if job.result else None
        if campaign_description_result is None:
            raise ValueError("Campaign description result is missing")

        available_channels = content_channel_service.search()
        dependencies = _AgentDependencies(
            brand=brand,
            prompt_template_name=prompt_template_name,
            available_channels=available_channels,
        )
        result = await _agent.run(
            user_prompt=[
                format_as_xml([job.user_input.prompt, campaign_description_result])
            ],
            deps=dependencies,
        )
        content_plan: AgentGeneratedPostingPlanResult = result.output
        return await _merge_to_campaign_generation_job_result(
            session_factory, job, content_plan
        )
    except Exception as e:
        logger.error(
            f"Failed to generate posting plan for job {job.id}: {e}",
            exc_info=True,
            extra={"job_id": job.id},
        )
        raise CampaignGenerationJobGenerationFailureException(
            job.id, f"Failed to generate content plan: {e}"
        ) from e


async def _merge_to_campaign_generation_job_result(
    session_factory: DbSessionFactory,
    job: CampaignGenerationJob,
    agent_posting_plan_result: AgentGeneratedPostingPlanResult,
) -> CampaignGenerationJobResult:
    current_result = job.get_result()
    if not current_result:
        raise CampaignGenerationJobResultNotFoundException(job.id)
    existing_items = await content_plan_item_service.search(session_factory, job.id)
    if len(existing_items) == 0:
        create_requests = [
            ContentPlanItemCreateRequest(
                job_id=job.id,
                description=agent_posting_plan_item.description,
                channel=agent_posting_plan_item.channel,
                content_type=agent_posting_plan_item.content_type,
                content_format=agent_posting_plan_item.content_format,
                image_urls=[],
                scheduled_at=agent_posting_plan_item.scheduled_at.astimezone(
                    UTC
                ).replace(tzinfo=None),
            )
            for agent_posting_plan_item in agent_posting_plan_result.plan_items
        ]
        existing_items = await content_plan_item_service.create_many(
            session_factory,
            job.id,
            create_requests,
        )
    current_result.content_plan_items = existing_items
    return current_result
