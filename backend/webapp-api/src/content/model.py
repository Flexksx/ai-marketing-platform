from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from lib.model import ContentChannelName, ContentFormat


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


class TextWithSingleImageContentData(BaseModel):
    caption: str
    image_url: str
    content_format: Literal[ContentFormat.TEXT_WITH_SINGLE_IMAGE] = (
        ContentFormat.TEXT_WITH_SINGLE_IMAGE
    )

    model_config = ConfigDict(from_attributes=True)


class TextOnlyContentData(BaseModel):
    caption: str
    content_format: Literal[ContentFormat.TEXT] = ContentFormat.TEXT

    model_config = ConfigDict(from_attributes=True)


ContentData = TextWithSingleImageContentData | TextOnlyContentData


class ContentCreateRequest(BaseModel):
    brand_id: str
    campaign_id: str | None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    scheduled_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentUpdateRequest(BaseModel):
    channel: ContentChannelName | None = None
    content_format: ContentFormat | None = None
    data: ContentData | None = None
    scheduled_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ContentListRequest(BaseModel):
    brand_id: str | None = None
    campaign_id: str | None = None
    channel: ContentChannelName | None = None
    scheduled_after: datetime | None = None
    scheduled_before: datetime | None = None
    limit: int | None = Field(default=10, ge=1, le=100)
    offset: int | None = Field(default=0, ge=0)

    model_config = ConfigDict(from_attributes=True)


class ContentResponse(BaseModel):
    id: str
    brand_id: str
    campaign_id: str | None = None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    scheduled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Content(BaseModel):
    id: str
    brand_id: str
    campaign_id: str | None = None
    channel: ContentChannelName
    content_format: ContentFormat
    data: ContentData
    created_at: datetime
    updated_at: datetime
    scheduled_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
