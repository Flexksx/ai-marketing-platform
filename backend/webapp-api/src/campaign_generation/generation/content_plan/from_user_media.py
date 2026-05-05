from datetime import UTC

from pydantic import BaseModel, ConfigDict
from pydantic_ai import Agent, ImageUrl, RunContext, format_as_xml

import src.brand.service as brand_service
import src.content_channel.service as content_channel_service
import src.content_plan_item.service as content_plan_item_service
from lib.ai_agents.schema import PydanticAiModel
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptService, PromptTemplateName
from src.brand.model import Brand
from src.campaign_generation.errors import (
    CampaignGenerationJobResultElementNotFoundException,
    CampaignGenerationJobResultNotFoundException,
)
from src.campaign_generation.generation.content_plan.model import (
    AgentGeneratedPostingPlanItem,
    AgentGeneratedPostingPlanResult,
)
from src.campaign_generation.generation.errors import (
    CampaignGenerationJobGenerationFailureException,
)
from src.campaign_generation.model import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentBriefCampaignGenerationJobResult,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from src.content_plan_item.model import ContentPlanItemCreateRequest
from src.shared.model import ContentChannel


class _AgentDependencies(BaseModel):
    brand: Brand
    user_input: UserMediaOnlyCampaignGenerationJobUserInput
    available_channels: list[ContentChannel]


class _ContentPlanItem(AgentGeneratedPostingPlanItem):
    image_url: str


class _ContentPlanOutput(AgentGeneratedPostingPlanResult):
    plan_items: list[_ContentPlanItem]
    model_config = ConfigDict(from_attributes=True)


_prompt_service = PromptService()

_agent: Agent[_AgentDependencies, _ContentPlanOutput] = Agent(
    model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
    deps_type=_AgentDependencies,
    output_type=_ContentPlanOutput,
)


@_agent.system_prompt
def _get_system_prompt(context: RunContext[_AgentDependencies]) -> str:
    return _prompt_service.render(
        PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP_FROM_USER_MEDIA,
        context.deps.model_dump(),
    )


async def generate_content_plan(
    job: CampaignGenerationJob,
    session_factory: DbSessionFactory,
) -> CampaignGenerationJobResult:
    brand = await brand_service.get(session_factory, job.brand_id)
    user_input = _get_user_input_or_raise(job)
    content_brief = _get_content_brief_or_raise(job)
    available_channels = content_channel_service.search()

    deps = _AgentDependencies(
        brand=brand,
        user_input=user_input,
        available_channels=available_channels,
    )
    ai_response = await _agent.run(
        user_prompt=[
            format_as_xml([user_input, content_brief]),
            *[ImageUrl(url) for url in user_input.image_urls],
        ],
        deps=deps,
    )
    posting_plan_result: _ContentPlanOutput = ai_response.output
    if not posting_plan_result:
        raise CampaignGenerationJobGenerationFailureException(
            job.id,
            "No output from agent for content plan generation",
        )
    return await _merge_campaign_result(session_factory, job, posting_plan_result)


def _get_user_input_or_raise(
    job: CampaignGenerationJob,
) -> UserMediaOnlyCampaignGenerationJobUserInput:
    if not isinstance(job.user_input, UserMediaOnlyCampaignGenerationJobUserInput):
        raise ValueError(f"User input is not a valid user input for job {job.id}")
    return job.user_input


def _get_content_brief_or_raise(
    job: CampaignGenerationJob,
) -> ContentBriefCampaignGenerationJobResult:
    description_result = job.get_description_result()
    if not description_result:
        raise CampaignGenerationJobResultElementNotFoundException(
            job.id, "description_result"
        )
    return description_result


async def _merge_campaign_result(
    session_factory: DbSessionFactory,
    job: CampaignGenerationJob,
    result: _ContentPlanOutput,
) -> CampaignGenerationJobResult:
    current_result = job.get_result()
    if not current_result:
        raise CampaignGenerationJobResultNotFoundException(job.id)
    existing_items = await content_plan_item_service.search(session_factory, job.id)
    if len(existing_items) == 0:
        create_requests = [
            ContentPlanItemCreateRequest(
                job_id=job.id,
                description=item.description,
                channel=item.channel,
                content_type=item.content_type,
                content_format=item.content_format,
                image_urls=[item.image_url],
                scheduled_at=item.scheduled_at.astimezone(UTC).replace(tzinfo=None),
            )
            for item in result.plan_items
        ]
        existing_items = await content_plan_item_service.create_many(
            session_factory,
            job.id,
            create_requests,
        )
    current_result.content_plan_items = existing_items
    return current_result
