from datetime import datetime
from typing import Annotated

import public
from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.brand.settings import (
    ContentPillarBusinessGoal,
)
from webapp_api_contract.campaign_generation import (
    AiGeneratedCampaignGenerationJobUserInput,
    CampaignGenerationJobWorkflowType,
    ProductLifestyleCampaignGenerationJobUserInput,
    UserMediaOnlyCampaignGenerationJobUserInput,
)
from webapp_api_contract.content_plan_items import ContentPlanItem
from webapp_api_contract.shared import ContentChannelName, JobStatus


@public.add
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


@public.add
class CampaignGenerationJobResult(BaseModel):
    content_brief: ContentBriefCampaignGenerationJobResult | None = None
    content_plan_items: list[ContentPlanItem] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


CampaignGenerationJobUserInput = Annotated[
    UserMediaOnlyCampaignGenerationJobUserInput
    | AiGeneratedCampaignGenerationJobUserInput
    | ProductLifestyleCampaignGenerationJobUserInput,
    Field(discriminator="workflow_type"),
]


@public.add
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
