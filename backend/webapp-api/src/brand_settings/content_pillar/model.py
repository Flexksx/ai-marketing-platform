import public
from pydantic import BaseModel, ConfigDict, Field
from strenum import StrEnum

from lib.utils import new_id


@public.add
class ContentPillarFunnelStage(StrEnum):
    AWARENESS = "AWARENESS"
    CONSIDERATION = "CONSIDERATION"
    CONVERSION = "CONVERSION"
    LOYALTY = "LOYALTY"


@public.add
class ContentPillarBusinessGoal(StrEnum):
    DRIVE_ENGAGEMENT = "DRIVE_ENGAGEMENT"
    INCREASE_CONVERSION = "INCREASE_CONVERSION"
    BUILD_TRUST = "BUILD_TRUST"
    GENERATE_LEADS = "GENERATE_LEADS"
    RETENTION = "RETENTION"


@public.add
class ContentPillarType(StrEnum):
    EDUCATION = "EDUCATION"
    PRODUCT_SERVICE = "PRODUCT_SERVICE"
    SOCIAL_PROOF = "SOCIAL_PROOF"
    BEHIND_THE_SCENES = "BEHIND_THE_SCENES"
    ENTERTAINMENT = "ENTERTAINMENT"
    COMMUNITY = "COMMUNITY"
    THOUGHT_LEADERSHIP = "THOUGHT_LEADERSHIP"


@public.add
class ContentTypeName(StrEnum):
    # Education
    TUTORIAL = "TUTORIAL"
    TIP = "TIP"
    GUIDE = "GUIDE"
    FRAMEWORK = "FRAMEWORK"
    MYTH = "MYTH"
    MISTAKE = "MISTAKE"
    INDUSTRY_INSIGHT = "INDUSTRY_INSIGHT"

    # Product / Service
    DEMO = "DEMO"
    FEATURE_HIGHLIGHT = "FEATURE_HIGHLIGHT"
    PRODUCT_USE = "PRODUCT_USE"
    BEFORE_AFTER = "BEFORE_AFTER"
    BENEFIT = "BENEFIT"
    COMPARISON = "COMPARISON"

    # Social Proof
    TESTIMONIAL = "TESTIMONIAL"
    REVIEW = "REVIEW"
    CASE_STUDY = "CASE_STUDY"
    CLIENT_STORY = "CLIENT_STORY"
    RESULT = "RESULT"
    SCREENSHOT = "SCREENSHOT"

    # Behind the Scenes
    FOUNDER_STORY = "FOUNDER_STORY"
    TEAM_HIGHLIGHT = "TEAM_HIGHLIGHT"
    PROCESS = "PROCESS"
    PRODUCT_BUILDING = "PRODUCT_BUILDING"
    DAILY_WORK = "DAILY_WORK"

    # Entertainment
    MEME = "MEME"
    TREND = "TREND"
    RELATABLE_POST = "RELATABLE_POST"
    HUMOR = "HUMOR"
    CULTURAL_COMMENTARY = "CULTURAL_COMMENTARY"

    # Thought Leadership
    OPINION = "OPINION"
    PREDICTION = "PREDICTION"
    HOT_TAKE = "HOT_TAKE"

    # Community
    POLL = "POLL"
    QUESTION = "QUESTION"
    DISCUSSION = "DISCUSSION"
    CHALLENGE = "CHALLENGE"


@public.add
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


@public.add
class ContentType(BaseModel):
    name: ContentTypeName = Field(default=ContentTypeName.BENEFIT)
    description: str = Field(default="")
