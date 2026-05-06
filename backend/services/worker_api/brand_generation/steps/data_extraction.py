import asyncio
import logging
import re

from fastapi import Depends
from pydantic_ai import Agent, ImageUrl

from services.worker_api.brand_generation.brand_data_generation import (
    BrandGenerationContentPillarResult,
    BrandGenerationJobAudienceProfilingResult,
    BrandGenerationJobTextualDescriptionResult,
    BrandGenerationJobToneOfVoiceProfilingResult,
    PositioningBrandDataResult,
)
from services.worker_api.brand_generation.steps.base import BrandGenerationBaseStep
from vozai.domain.brand import BrandCreateRequest, BrandData
from vozai.domain.brand_extraction import (
    BrandGenerationJob,
    BrandGenerationJobResultElementNotFoundError,
    BrandGenerationJobResultNotFoundError,
    BrandGenerationResult,
)
from vozai.domain.brand_settings import (
    BrandToneOfVoice,
    PositioningBrandData,
)
from vozai.lib.ai_agents.schema import PydanticAiModel
from vozai.lib.prompts import PromptService, PromptTemplateName
from vozai.lib.scraper.model import ScrapeResult


logger = logging.getLogger(__name__)


class BrandDataExtractionStep(BrandGenerationBaseStep):
    def __init__(
        self,
        prompt_service: PromptService = Depends(),
    ):
        self.prompt_service = prompt_service
        self.__core_identity_agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LATEST,
            system_prompt=self.prompt_service.render(
                PromptTemplateName.BRAND_GENERATION_TEXTUAL_DESCRIPTION, {}
            ),
            output_type=BrandGenerationJobTextualDescriptionResult,
        )
        self.__strategy_agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
            system_prompt=self.prompt_service.render(
                PromptTemplateName.BRAND_GENERATION_STRATEGIC_PROFILING, {}
            ),
            output_type=PositioningBrandDataResult,
        )
        self.__tone_of_voice_agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
            system_prompt=self.prompt_service.render(
                PromptTemplateName.BRAND_GENERATION_TONE_OF_VOICE_PROFILING, {}
            ),
            output_type=BrandGenerationJobToneOfVoiceProfilingResult,
        )
        self.__audience_agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
            system_prompt=self.prompt_service.render(
                PromptTemplateName.BRAND_GENERATION_AUDIENCE_PROFILING, {}
            ),
            output_type=BrandGenerationJobAudienceProfilingResult,
        )
        self.__marketing_agent = Agent(
            model=PydanticAiModel.GEMINI_FLASH_LITE_LATEST,
            system_prompt=self.prompt_service.render(
                PromptTemplateName.BRAND_GENERATION_MARKETING_PROFILING, {}
            ),
            output_type=BrandGenerationContentPillarResult,
        )

    async def execute(self, job: BrandGenerationJob) -> BrandGenerationResult:
        logger.info(
            f"Starting brand extraction for job {job.id}",
            extra={"job_id": job.id},
        )
        scrape_result = self.__get_scraper_result_or_raise(job)

        results = await self.__run_brand_agents(scrape_result)

        brand_create_request = self.__merge_extraction_results(scrape_result, *results)

        current_result = self.__get_result_or_raise(job)
        current_result.brand_data = brand_create_request

        return current_result

    def __filter_supported_image_urls(self, urls: list[str]) -> list[str]:
        supported_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        filtered = []

        for url in urls:
            if not url:
                continue

            url_lower = url.lower()
            has_supported_extension = any(
                url_lower.endswith(ext)
                or f"/{ext[1:]}" in url_lower
                or f".{ext[1:]}" in url_lower
                for ext in supported_extensions
            )

            is_svg = ".svg" in url_lower

            if has_supported_extension and not is_svg:
                filtered.append(url)
            else:
                logger.debug(f"Filtering out unsupported image format: {url}")

        return filtered

    def __sanitize_text(self, text: str) -> str:
        if not text:
            return text

        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s<>"{}|\\^`\[\]]*'

        sanitized = re.sub(url_pattern, "", text)

        sanitized = re.sub(r"\s+", " ", sanitized)
        sanitized = re.sub(r"\n\s*\n", "\n\n", sanitized)
        sanitized = sanitized.strip()

        original_length = len(text)
        sanitized_length = len(sanitized)
        reduction = original_length - sanitized_length

        if reduction > 0:
            reduction_pct = reduction / original_length * 100
            logger.info(
                f"Sanitized text: removed {reduction} chars "
                f"({reduction_pct:.1f}% reduction) by removing external links"
            )

        return sanitized

    async def __run_brand_agents(self, scrape_result: ScrapeResult):
        sanitized_text = self.__sanitize_text(scrape_result.text)
        image_urls = [scrape_result.screenshot] if scrape_result.screenshot else []
        extraction_input = [
            sanitized_text,
            *self.__get_as_image_urls_for_agent(image_urls),
        ]

        try:
            (
                core_result,
                strategy_result,
                tone_result,
                audiences_result,
            ) = await asyncio.gather(
                self.__core_identity_agent.run(extraction_input),
                self.__strategy_agent.run(extraction_input),
                self.__tone_of_voice_agent.run(extraction_input),
                self.__audience_agent.run(extraction_input),
            )
            marketing_input = [
                *extraction_input,
                audiences_result.output.model_dump_json(),
            ]
            marketing_result = await self.__marketing_agent.run(marketing_input)

            return [
                core_result.output,
                strategy_result.output,
                tone_result.output,
                audiences_result.output,
                marketing_result.output,
            ]
        except Exception as error:
            logger.error(f"Pillar extraction failed: {error}", exc_info=True)
            raise

    @staticmethod
    def __merge_extraction_results(
        scrape_result,
        core_result: BrandGenerationJobTextualDescriptionResult,
        strategy_result: PositioningBrandDataResult,
        tone_result: BrandGenerationJobToneOfVoiceProfilingResult,
        audiences_result: BrandGenerationJobAudienceProfilingResult,
        content_pillars_result: BrandGenerationContentPillarResult,
    ) -> BrandCreateRequest:
        positioning_result = PositioningBrandData(
            points_of_parity=strategy_result.points_of_parity,
            points_of_difference=strategy_result.points_of_difference,
            product_description=strategy_result.product_description,
            description=core_result.description,
        )

        tone = BrandToneOfVoice(
            sentence_length_preference=tone_result.sentence_length_preference,
            industry_jargon_usage_level=tone_result.industry_jargon_usage_level,
            formality_level=tone_result.formality_level,
            irreverence_level=tone_result.irreverence_level,
            enthusiasm_level=tone_result.enthusiasm_level,
            humour_level=tone_result.humour_level,
            sensory_keywords=tone_result.sensory_keywords,
            excluded_words=tone_result.excluded_words,
            signature_words=tone_result.signature_words,
        )

        return BrandCreateRequest(
            name=core_result.name,
            data=BrandData(
                logo_url=scrape_result.logo or "",
                media_urls=scrape_result.image_urls,
                colors=core_result.colors,
                brand_mission=core_result.brand_mission,
                archetype=core_result.archetype,
                audiences=audiences_result.audiences,
                tone_of_voice=tone,
                positioning=positioning_result,
                content_pillars=content_pillars_result.content_pillars,
                locale=core_result.locale,
            ),
        )

    def __get_result_or_raise(self, job: BrandGenerationJob) -> BrandGenerationResult:
        result = job.result
        if not result:
            raise BrandGenerationJobResultNotFoundError(
                job_id=job.id,
            )
        return result

    def __get_scraper_result_or_raise(self, job: BrandGenerationJob) -> ScrapeResult:
        result = self.__get_result_or_raise(job)
        scraper_result = result.scraper_result
        if not scraper_result:
            raise BrandGenerationJobResultElementNotFoundError(
                job_id=job.id,
                element_name="scraper_result",
            )
        return scraper_result

    def __get_as_image_urls_for_agent(self, urls: list[str]) -> list[ImageUrl]:
        return [ImageUrl(url=url) for url in urls]
