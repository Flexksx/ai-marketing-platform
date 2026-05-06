import public
from strenum import StrEnum


@public.add
class ContentGenerationJobWorkflowType(StrEnum):
    TEXT_ONLY = "TEXT_ONLY"
    USER_MEDIA = "USER_MEDIA"
