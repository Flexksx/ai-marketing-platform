from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract.campaign_generation import (
    CampaignGenerationJobResult,
    CampaignGenerationJobUserInput,
    ContentBriefCampaignGenerationJobResult,
)
from webapp_api_contract.content_plan_items import ContentPlanItem
from webapp_api_contract.shared import CampaignGenerationJobWorkflowType, JobStatus


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
