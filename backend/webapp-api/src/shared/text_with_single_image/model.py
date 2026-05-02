import public
from pydantic import BaseModel

from webapp_api_contract.shared import ContentChannelName, ContentFormat


@public.add
class TextWithSingleImageContent(BaseModel):
    text: str
    image_url: str
    channel: ContentChannelName
    content_type: ContentFormat
