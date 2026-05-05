import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic_ai import Agent, ImageUrl, RunContext, format_as_xml

import src.brand.service as brand_service
import src.content_channel.service as content_channel_service
import src.content_plan_item.service as content_plan_item_service
from lib import prompts
from lib.ai_agents import PydanticAiModel
from lib.model import ContentChannelName, ContentFormat
from lib.prompts import PromptTemplateName
from src.brand.model import Brand, ContentPillarType
from src.campaign_generation.errors import (
    CampaignGenerationJobResultElementNotFoundException,
    CampaignGenerationJobResultNotFoundException,
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
from src.content.model import ContentTypeName
from src.content_channel.model import ContentChannel
from src.content_plan_item.model import ContentPlanItemCreateRequest


logger = logging.getLogger(__name__)


class _PostingPlanItem(BaseModel):
    content_pillar_type: ContentPillarType
    content_type: ContentTypeName
    content_format: ContentFormat
    channel: ContentChannelName
    scheduled_at: datetime
    description: str

    model_config = ConfigDict(from_attributes=True)


class _PostingPlanResult(BaseModel):
    plan_items: list[_PostingPlanItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class _UserMediaPlanItem(_PostingPlanItem):
    image_url: str


class _UserMediaPlanResult(_PostingPlanResult):
    plan_items: list[_UserMediaPlanItem]

    model_config = ConfigDict(from_attributes=True)


class _AiGeneratedAgentDeps(BaseModel):
    brand: Brand
    available_channels: list[ContentChannel]


class _UserMediaAgentDeps(BaseModel):
    brand: Brand
    user_input: UserMediaOnlyCampaignGenerationJobUserInput
    available_channels: list[ContentChannel]


_ai_generated_agent: Agent[_AiGeneratedAgentDeps, _PostingPlanResult] = Agent(  # ty:ignore[invalid-assignment]
    model=PydanticAiModel.GEMINI_FLASH_LATEST,
    deps_type=_AiGeneratedAgentDeps,
    output_type=_PostingPlanResult,
)

_user_media_agent: Agent[_UserMediaAgentDeps, _UserMediaPlanResult] = Agent(  # ty:ignore[invalid-assignment]
    model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
    deps_type=_UserMediaAgentDeps,
    output_type=_UserMediaPlanResult,
)


@_ai_generated_agent.system_prompt
def _ai_generated_system_prompt(context: RunContext[_AiGeneratedAgentDeps]) -> str:
    return prompts.render(
        PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP,
        context.deps.model_dump(),
    )


@_user_media_agent.system_prompt
def _user_media_system_prompt(context: RunContext[_UserMediaAgentDeps]) -> str:
    return prompts.render(
        PromptTemplateName.CAMPAIGN_GENERATION_CONTENT_PLAN_STEP_FROM_USER_MEDIA,
        context.deps.model_dump(),
    )


async def generate_ai_content_plan(
    job: CampaignGenerationJob,
) -> CampaignGenerationJobResult:
    try:
        brand = await brand_service.get(job.brand_id)
        content_brief = job.result.content_brief if job.result else None
        if content_brief is None:
            raise ValueError("Campaign content brief is missing")

        deps = _AiGeneratedAgentDeps(
            brand=brand,
            available_channels=content_channel_service.search(),
        )
        result = await _ai_generated_agent.run(
            user_prompt=[format_as_xml([job.user_input.prompt, content_brief])],
            deps=deps,
        )
        return await _merge_plan_items(
            job, result.output.plan_items, image_urls_per_item=None
        )
    except Exception as e:
        logger.error(
            f"Failed to generate content plan for job {job.id}: {e}",
            exc_info=True,
            extra={"job_id": job.id},
        )
        raise CampaignGenerationJobGenerationFailureException(
            job.id, f"Failed to generate content plan: {e}"
        ) from e


async def generate_user_media_content_plan(
    job: CampaignGenerationJob,
) -> CampaignGenerationJobResult:
    brand = await brand_service.get(job.brand_id)
    user_input = _get_user_media_input_or_raise(job)
    content_brief = _get_content_brief_or_raise(job)

    deps = _UserMediaAgentDeps(
        brand=brand,
        user_input=user_input,
        available_channels=content_channel_service.search(),
    )
    ai_response = await _user_media_agent.run(
        user_prompt=[
            format_as_xml([user_input, content_brief]),
            *[ImageUrl(url) for url in user_input.image_urls],
        ],
        deps=deps,
    )
    plan_output: _UserMediaPlanResult = ai_response.output
    if not plan_output:
        raise CampaignGenerationJobGenerationFailureException(
            job.id,
            "No output from agent for content plan generation",
        )
    image_urls_by_item = {item: item.image_url for item in plan_output.plan_items}
    return await _merge_plan_items(
        job, plan_output.plan_items, image_urls_per_item=image_urls_by_item
    )


def _get_user_media_input_or_raise(
    job: CampaignGenerationJob,
) -> UserMediaOnlyCampaignGenerationJobUserInput:
    if not isinstance(job.user_input, UserMediaOnlyCampaignGenerationJobUserInput):
        raise ValueError(f"User input is not valid for job {job.id}")
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


async def _merge_plan_items(
    job: CampaignGenerationJob,
    plan_items: Sequence[_PostingPlanItem],
    image_urls_per_item: dict[Any, str] | None,
) -> CampaignGenerationJobResult:
    current_result = job.get_result()
    if not current_result:
        raise CampaignGenerationJobResultNotFoundException(job.id)
    existing_items = await content_plan_item_service.search(job.id)
    if len(existing_items) == 0:
        create_requests = [
            ContentPlanItemCreateRequest(
                job_id=job.id,
                description=item.description,
                channel=item.channel,
                content_type=item.content_type,
                content_format=item.content_format,
                image_urls=(
                    [image_urls_per_item[item]]
                    if image_urls_per_item and item in image_urls_per_item
                    else []
                ),
                scheduled_at=item.scheduled_at.astimezone(UTC).replace(tzinfo=None),
            )
            for item in plan_items
        ]
        existing_items = await content_plan_item_service.create_many(
            job.id, create_requests
        )
    current_result.content_plan_items = existing_items
    return current_result
