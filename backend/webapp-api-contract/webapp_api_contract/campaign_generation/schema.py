from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.campaign_generation.model import (
    CampaignGenerationJobResult,
    CampaignGenerationJobUserInput,
)
from webapp_api_contract.shared import CampaignGenerationJobWorkflowType, JobStatus


class CampaignGenerationJobCreateRequest(BaseModel):
    brand_id: str
    workflow_type: CampaignGenerationJobWorkflowType
    user_input: CampaignGenerationJobUserInput

    model_config = ConfigDict(from_attributes=True)


class CampaignCreationJobUpdateInput(BaseModel):
    status: JobStatus
    result: CampaignGenerationJobResult | None = None

    model_config = ConfigDict(from_attributes=True)


class CampaignGenerationJobResponse(BaseModel):
    id: str
    brand_id: str
    status: JobStatus
    user_input: CampaignGenerationJobUserInput
    result: CampaignGenerationJobResult
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


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


class CampaignCreationAcceptRequest(BaseModel):
    posting_plan_modifications: list[ContentPlanItemModification] = Field(
        default=[],
        description="List of modifications to apply to posting plan items",
    )
