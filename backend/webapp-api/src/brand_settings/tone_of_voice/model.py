from enum import StrEnum

import public
from pydantic import BaseModel, ConfigDict, Field


@public.add
class ToneOfVoiceDimensionName(StrEnum):
    FORMALITY = "FORMALITY"
    HUMOUR = "HUMOUR"
    IRREVERENCE = "IRREVERENCE"
    ENTHUSIASM = "ENTHUSIASM"
    JARGON = "JARGON"


@public.add
class ToneOfVoiceDimensionLevel(BaseModel):
    scale_number: int
    name: str
    description: str


@public.add
class ToneOfVoiceDimension(BaseModel):
    name: ToneOfVoiceDimensionName
    levels: list[ToneOfVoiceDimensionLevel]

    model_config = ConfigDict(frozen=True)


@public.add
class SentenceLengthPreference(StrEnum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"


@public.add
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
