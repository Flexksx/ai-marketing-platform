from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brand_settings import ContentPillarBusinessGoal
from webapp_api_contract.content_plan_items import ContentPlanItem
from webapp_api_contract.shared import (
    CampaignGenerationJobWorkflowType,
    ContentChannelName,
    JobStatus,
)


class BaseCampaignGenerationJobUserInput(BaseModel):
    prompt: str = Field(
        ..., description="User's input about what they want the campaign to be about"
    )
    start_date: datetime = Field(..., description="Campaign start date")
    end_date: datetime = Field(..., description="Campaign end date")
    channels: list[ContentChannelName] = Field(
        ..., description="List of channels the campaign is going to be posted to"
    )

    model_config = ConfigDict(from_attributes=True)


class UserMediaOnlyCampaignGenerationJobUserInput(BaseCampaignGenerationJobUserInput):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY] = (
        CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY
    )
    image_urls: list[str]


class AiGeneratedCampaignGenerationJobUserInput(BaseCampaignGenerationJobUserInput):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.AI_GENERATED] = (
        CampaignGenerationJobWorkflowType.AI_GENERATED
    )


class ProductLifestyleCampaignGenerationJobUserInput(
    BaseCampaignGenerationJobUserInput
):
    workflow_type: Literal[CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE] = (
        CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE
    )
    image_urls: list[str] = Field(
        ...,
        description="List of product image URLs to be preserved in generated lifestyle images",
    )


CampaignGenerationJobUserInput = Annotated[
    UserMediaOnlyCampaignGenerationJobUserInput
    | AiGeneratedCampaignGenerationJobUserInput
    | ProductLifestyleCampaignGenerationJobUserInput,
    Field(discriminator="workflow_type"),
]


class ContentBriefCampaignGenerationJobResult(BaseModel):
    name: str
    description: str
    goal: ContentPillarBusinessGoal
    target_audience_ids: list[str] = Field(default_factory=list)
    content_pillar_ids: list[str] = Field(default_factory=list)
    start_date: datetime
    end_date: datetime
    channels: list[ContentChannelName]

    model_config = ConfigDict(from_attributes=True)


class CampaignGenerationJobResult(BaseModel):
    content_brief: ContentBriefCampaignGenerationJobResult | None = None
    content_plan_items: list[ContentPlanItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class CampaignGenerationJob(BaseModel):
    id: str
    brand_id: str
    status: JobStatus
    workflow_type: CampaignGenerationJobWorkflowType
    user_input: CampaignGenerationJobUserInput
    result: CampaignGenerationJobResult = Field(
        default_factory=CampaignGenerationJobResult
    )
    created_at: datetime
    updated_at: datetime

    def get_result(self) -> CampaignGenerationJobResult | None:
        return self.result

    def get_description_result(self) -> ContentBriefCampaignGenerationJobResult | None:
        result = self.get_result()
        return result.content_brief if result else None

    def get_content_plan_items(self) -> list[ContentPlanItem] | None:
        result = self.get_result()
        return result.content_plan_items if result else None

    model_config = ConfigDict(from_attributes=True)


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
