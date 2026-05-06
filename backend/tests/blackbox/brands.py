import public
from faker import Faker
from pydantic_extra_types.language_code import LanguageAlpha2

from vozai.domain.brand import BrandColor, BrandData
from vozai.domain.brand_archetype.model import BrandArchetypeName
from vozai.domain.brand_settings import (
    BrandAudience,
    BrandAudienceAgeRange,
    BrandAudienceGender,
    BrandAudienceIncomeRange,
    BrandToneOfVoice,
    SentenceLengthPreference,
)


fake = Faker()


@public.add
class BrandMockFactory:
    @staticmethod
    def create_tone_of_voice() -> BrandToneOfVoice:
        return BrandToneOfVoice(
            formality_level=fake.random_int(min=1, max=4),
            humour_level=fake.random_int(min=1, max=4),
            irreverence_level=fake.random_int(min=1, max=4),
            enthusiasm_level=fake.random_int(min=1, max=4),
            industry_jargon_usage_level=fake.random_int(min=1, max=4),
            sensory_keywords=[fake.word() for _ in range(3)],
            excluded_words=[fake.word() for _ in range(2)],
            signature_words=[fake.word() for _ in range(2)],
            sentence_length_preference=fake.random_element(
                elements=list(SentenceLengthPreference)
            ),
        )

    @classmethod
    def create_brand_data(cls) -> BrandData:
        return BrandData(
            logo_url=fake.image_url(),
            media_urls=[fake.image_url() for _ in range(2)],
            colors=[
                BrandColor(name="Primary", hex_value=fake.hex_color()),
                BrandColor(name="Secondary", hex_value=fake.hex_color()),
            ],
            brand_mission=fake.sentence(nb_words=10),
            archetype=fake.random_element(elements=list(BrandArchetypeName)),
            locale=LanguageAlpha2("en"),
            audiences=[
                cls.create_brand_audience(),
                cls.create_brand_audience(),
            ],
            tone_of_voice=BrandMockFactory.create_tone_of_voice(),
        )

    @classmethod
    def create_brand_audience(cls) -> BrandAudience:
        return BrandAudience(
            name=fake.word(),
            age_range=fake.random_element(elements=list(BrandAudienceAgeRange)),
            gender=fake.random_element(elements=list(BrandAudienceGender)),
            income_range=fake.random_element(elements=list(BrandAudienceIncomeRange)),
            pain_points=[fake.word() for _ in range(3)],
            objections=[fake.word() for _ in range(2)],
        )
