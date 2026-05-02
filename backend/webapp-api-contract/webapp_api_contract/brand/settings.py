from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from webapp_api_contract._utils import new_id
from webapp_api_contract.shared import ContentChannelName


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


class ToneOfVoiceDimensionName(StrEnum):
    FORMALITY = "FORMALITY"
    HUMOUR = "HUMOUR"
    IRREVERENCE = "IRREVERENCE"
    ENTHUSIASM = "ENTHUSIASM"
    JARGON = "JARGON"


class ToneOfVoiceDimensionLevel(BaseModel):
    scale_number: int
    name: str
    description: str


class ToneOfVoiceDimension(BaseModel):
    name: ToneOfVoiceDimensionName
    levels: list[ToneOfVoiceDimensionLevel]

    model_config = ConfigDict(frozen=True)


class SentenceLengthPreference(StrEnum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"


class BrandToneOfVoice(BaseModel):
    formality_level: int = Field(default=1, ge=1, le=4)
    humour_level: int = Field(default=1, ge=1, le=4)
    irreverence_level: int = Field(default=1, ge=1, le=4)
    enthusiasm_level: int = Field(default=1, ge=1, le=4)
    industry_jargon_usage_level: int = Field(default=1, ge=1, le=4)
    sensory_keywords: list[str] = Field(default_factory=list)
    excluded_words: list[str] = Field(default_factory=list)
    signature_words: list[str] = Field(default_factory=list)
    sentence_length_preference: SentenceLengthPreference = Field(
        default=SentenceLengthPreference.MEDIUM
    )

    model_config = ConfigDict(frozen=True)


class PositioningBrandData(BaseModel):
    description: str = Field(default="")
    points_of_difference: list[str] = Field(default_factory=list)
    points_of_parity: list[str] = Field(default_factory=list)
    product_description: str = Field(default="")

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


class ContentType(BaseModel):
    name: ContentTypeName = Field(default=ContentTypeName.BENEFIT)
    description: str = Field(default="")
