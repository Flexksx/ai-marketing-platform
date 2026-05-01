from datetime import datetime

import public
from pydantic import BaseModel, ConfigDict, Field

from aimarketing.domain.campaign_generation.base.model import (
    CampaignGenerationJobWorkflowType,
)
from aimarketing.domain.campaign_generation.model import (
    CampaignGenerationJobResult,
    CampaignGenerationJobUserInput,
)
from aimarketing.lib.job.model import JobStatus


@public.add
class CampaignGenerationJobCreateRequest(BaseModel):
    brand_id: str
    workflow_type: CampaignGenerationJobWorkflowType
    user_input: CampaignGenerationJobUserInput

    model_config = ConfigDict(from_attributes=True)


@public.add
class CampaignCreationJobUpdateInput(BaseModel):
    status: JobStatus
    result: CampaignGenerationJobResult | None = None

    model_config = ConfigDict(from_attributes=True)


@public.add
class CampaignGenerationJobResponse(BaseModel):
    id: str
    brand_id: str
    status: JobStatus
    user_input: CampaignGenerationJobUserInput
    result: CampaignGenerationJobResult
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


@public.add
class ContentPlanItemModification(BaseModel):
    item_id: str = Field(..., description="ID of the posting plan item to modify")
    caption: str | None = Field(
        default=None, description="Modified caption for the post"
    )
    image_url: str | None = Field(
        default=None, description="Modified image URL for the post"
    )
    scheduled_at: datetime | None = Field(
        default=None, description="Modified scheduled date and time for the post"
    )


@public.add
class CampaignCreationAcceptRequest(BaseModel):
    posting_plan_modifications: list[ContentPlanItemModification] = Field(
        default=[],
        description="List of modifications to apply to posting plan items",
    )
