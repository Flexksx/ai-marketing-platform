from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from lib.utils import new_id
from src.brand.archetype.model import BrandArchetypeName
from src.shared.model import ContentChannelName


class ContentTypeName(StrEnum):
    TUTORIAL = "TUTORIAL"
    TIP = "TIP"
    GUIDE = "GUIDE"
    FRAMEWORK = "FRAMEWORK"
    MYTH = "MYTH"
    MISTAKE = "MISTAKE"
    INDUSTRY_INSIGHT = "INDUSTRY_INSIGHT"
    DEMO = "DEMO"
    FEATURE_HIGHLIGHT = "FEATURE_HIGHLIGHT"
    PRODUCT_USE = "PRODUCT_USE"
    BEFORE_AFTER = "BEFORE_AFTER"
    BENEFIT = "BENEFIT"
    COMPARISON = "COMPARISON"
    TESTIMONIAL = "TESTIMONIAL"
    REVIEW = "REVIEW"
    CASE_STUDY = "CASE_STUDY"
    CLIENT_STORY = "CLIENT_STORY"
    RESULT = "RESULT"
    SCREENSHOT = "SCREENSHOT"
    FOUNDER_STORY = "FOUNDER_STORY"
    TEAM_HIGHLIGHT = "TEAM_HIGHLIGHT"
    PROCESS = "PROCESS"
    PRODUCT_BUILDING = "PRODUCT_BUILDING"
    DAILY_WORK = "DAILY_WORK"
    MEME = "MEME"
    TREND = "TREND"
    RELATABLE_POST = "RELATABLE_POST"
    HUMOR = "HUMOR"
    CULTURAL_COMMENTARY = "CULTURAL_COMMENTARY"
    OPINION = "OPINION"
    PREDICTION = "PREDICTION"
    HOT_TAKE = "HOT_TAKE"
    POLL = "POLL"
    QUESTION = "QUESTION"
    DISCUSSION = "DISCUSSION"
    CHALLENGE = "CHALLENGE"


class ContentType(BaseModel):
    name: ContentTypeName = Field(default=ContentTypeName.BENEFIT)
    description: str = Field(default="")


class BrandAudienceAgeRange(StrEnum):
    TEENS = "TEENS"
    YOUNG_ADULTS = "YOUNG_ADULTS"
    ADULTS = "ADULTS"
    MIDDLE_AGED = "MIDDLE_AGED"
    SENIORS = "SENIORS"
    ANY = "ANY"


class BrandAudienceGender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ANY = "ANY"


class BrandAudienceIncomeRange(StrEnum):
    LOW_INCOME = "LOW_INCOME"
    MIDDLE_INCOME = "MIDDLE_INCOME"
    UPPER_MIDDLE_INCOME = "UPPER_MIDDLE_INCOME"
    HIGH_INCOME = "HIGH_INCOME"
    ANY = "ANY"


class BrandAudience(BaseModel):
    id: str = Field(default_factory=new_id)
    name: str = Field(default="")
    age_range: BrandAudienceAgeRange = Field(BrandAudienceAgeRange.ANY)
    gender: BrandAudienceGender = Field(BrandAudienceGender.ANY)
    income_range: BrandAudienceIncomeRange = Field(BrandAudienceIncomeRange.ANY)
    pain_points: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    channels: list[ContentChannelName] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


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


class PositioningBrandData(BaseModel):
    description: str = Field(default="")
    points_of_difference: list[str] = Field(default_factory=list)
    points_of_parity: list[str] = Field(default_factory=list)
    product_description: str = Field(default="")

    model_config = ConfigDict(from_attributes=True)


class BrandToneOfVoice(BaseModel):
    archetype: BrandArchetypeName | None = Field(default=None)
    jargon_density: int = Field(default=1, ge=1, le=4)
    visual_density: int = Field(default=1, ge=1, le=4)
    must_use_words: list[str] = Field(default_factory=list)
    forbidden_words: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class BrandColor(BaseModel):
    name: str
    hex_value: str


class BrandData(BaseModel):
    logo_url: str | None = Field(default=None)
    website_url: str | None = Field(default=None)
    media_urls: list[str] = Field(default_factory=list)
    colors: list[BrandColor] = Field(default_factory=list)
    brand_mission: str | None = Field(default=None)
    locale: LanguageAlpha2 | None = Field(default=None)
    audiences: list[BrandAudience] = Field(default_factory=list)
    content_pillars: list[ContentPillar] = Field(default_factory=list)
    tone_of_voice: BrandToneOfVoice = Field(default_factory=BrandToneOfVoice)
    positioning: PositioningBrandData = Field(default_factory=PositioningBrandData)

    model_config = ConfigDict(from_attributes=True)


class BrandCreateRequest(BaseModel):
    name: str
    data: BrandData

    model_config = ConfigDict(from_attributes=True)


class BrandSearchRequest(BaseModel):
    user_id: str
    name: str | None = None
    limit: int | None = Field(default=5, ge=1, le=1000)
    offset: int | None = Field(default=0, ge=0)


class BrandResponse(BaseModel):
    id: str
    name: str
    data: BrandData | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BrandUpdateRequest(BaseModel):
    name: str | None = None
    data: BrandData | None = None

    model_config = ConfigDict(from_attributes=True)


class Brand(BaseModel):
    id: str
    user_id: str
    name: str
    data: BrandData = Field(default_factory=BrandData)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
