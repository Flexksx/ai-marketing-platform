from enum import StrEnum

from pydantic import BaseModel, Field


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


class ContentType(BaseModel):
    name: ContentTypeName = Field(default=ContentTypeName.BENEFIT)
    description: str = Field(default="")
