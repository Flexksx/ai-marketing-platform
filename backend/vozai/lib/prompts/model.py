import public
from pydantic import BaseModel, ConfigDict
from strenum import StrEnum

from vozai.domain.brand_archetype.model import BrandArchetype, BrandArchetypeName
from vozai.domain.brand_settings import ContentType
from vozai.domain.brand_settings.content_pillar.model import ContentTypeName
from vozai.domain.brand_settings.tone_of_voice.model import (
    ToneOfVoiceDimension,
    ToneOfVoiceDimensionName,
)


@public.add
class PromptConfigError(Exception):
    pass


@public.add
class PromptTemplateName(StrEnum):
    TEXT_WITH_SINGLE_IMAGE_CAPTION = "content/text_with_single_image/caption.j2"
    TEXT_WITH_SINGLE_IMAGE_AI_GENERATED_IMAGE = (
        "content/text_with_single_image/ai_generated_image.j2"
    )
    TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE_IMAGE = (
        "content/text_with_single_image/product_lifestyle_image.j2"
    )
    BRAND_GENERATION_TEXTUAL_DESCRIPTION = (
        "brand_generation/data_extraction/textual_description.j2"
    )
    BRAND_GENERATION_TONE_OF_VOICE_PROFILING = (
        "brand_generation/data_extraction/tone_of_voice_profiling.j2"
    )
    BRAND_GENERATION_STRATEGIC_PROFILING = (
        "brand_generation/data_extraction/strategic_profiling.j2"
    )
    BRAND_GENERATION_MARKETING_PROFILING = (
        "brand_generation/data_extraction/marketing_profiling.j2"
    )
    BRAND_GENERATION_AUDIENCE_PROFILING = (
        "brand_generation/data_extraction/audience_profiling.j2"
    )
    CAMPAIGN_GENERATION_DESCRIPTION_STEP = (
        "campaign_generation/campaign_description_step.j2"
    )
    CAMPAIGN_GENERATION_CONTENT_PLAN_STEP = "campaign_generation/content_plan_step.j2"
    CAMPAIGN_GENERATION_CONTENT_PLAN_STEP_FROM_USER_MEDIA = (
        "campaign_generation/content_plan_from_user_media.j2"
    )


class PromptLibraries(BaseModel):
    tone_library: dict[ToneOfVoiceDimensionName, ToneOfVoiceDimension]
    archetype_library: dict[BrandArchetypeName, BrandArchetype]
    content_type_library: dict[ContentTypeName, ContentType]

    model_config = ConfigDict(frozen=True)
