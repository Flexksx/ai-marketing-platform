from typing import Literal

from pydantic import BaseModel, ConfigDict

from webapp_api_contract.shared import ContentFormat


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
