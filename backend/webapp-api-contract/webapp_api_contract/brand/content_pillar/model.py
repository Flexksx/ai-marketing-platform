from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract._utils import new_id
from webapp_api_contract.brand.content_type import ContentTypeName


class ContentPillarFunnelStage(StrEnum):
    AWARENESS = "AWARENESS"
    CONSIDERATION = "CONSIDERATION"
    CONVERSION = "CONVERSION"
    LOYALTY = "LOYALTY"


class ContentPillarBusinessGoal(StrEnum):
    DRIVE_ENGAGEMENT = "DRIVE_ENGAGEMENT"
    INCREASE_CONVERSION = "INCREASE_CONVERSION"
    BUILD_TRUST = "BUILD_TRUST"
    GENERATE_LEADS = "GENERATE_LEADS"
    RETENTION = "RETENTION"


class ContentPillarType(StrEnum):
    EDUCATION = "EDUCATION"
    PRODUCT_SERVICE = "PRODUCT_SERVICE"
    SOCIAL_PROOF = "SOCIAL_PROOF"
    BEHIND_THE_SCENES = "BEHIND_THE_SCENES"
    ENTERTAINMENT = "ENTERTAINMENT"
    COMMUNITY = "COMMUNITY"
    THOUGHT_LEADERSHIP = "THOUGHT_LEADERSHIP"


class ContentPillar(BaseModel):
    id: str = Field(default_factory=new_id)
    name: str = Field(default="")
    business_goal: ContentPillarBusinessGoal = Field(
        default=ContentPillarBusinessGoal.BUILD_TRUST
    )
    type: ContentPillarType = Field(default=ContentPillarType.THOUGHT_LEADERSHIP)
    funnel_stage: ContentPillarFunnelStage = Field(
        default=ContentPillarFunnelStage.LOYALTY
    )
    content_types: list[ContentTypeName] = Field(default_factory=list)
    audience_ids: list[str] = Field(default_factory=list)
    hooks: list[str] = Field(default_factory=list)
    calls_to_action: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
