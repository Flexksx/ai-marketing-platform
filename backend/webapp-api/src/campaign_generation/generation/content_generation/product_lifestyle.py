import asyncio
import logging

import public
from fastapi import Depends
from pydantic_ai import format_as_xml

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.campaign_generation.model import CampaignGenerationJob
from src.shared.text_with_single_image import (
    TextWithSingleImageContentGenerator,
)
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJobResult,
    ContentPlanItem,
)
from webapp_api_contract.content import TextWithSingleImageContentData
from webapp_api_contract.content_plan_items import ContentPlanItemUpdateRequest
from webapp_api_contract.shared import JobStatus


logger = logging.getLogger(__name__)


@public.add
class ProductLifestyleContentPlanItemGenerator:
    def __init__(
        self,
        session_factory: DbSessionFactory = Depends(),
        text_with_single_image_service: TextWithSingleImageContentGenerator = Depends(),
    ):
        self.session_factory = session_factory
        self.text_with_single_image_service = text_with_single_image_service

    async def generate(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        if not job.result or not job.result.content_plan_items:
            raise ValueError("Content plan items not found")

        plan_items = job.result.content_plan_items
        product_image_urls = self.__get_product_image_urls(job)

        logger.info(
            f"Generating {len(plan_items)} product lifestyle posts "
            f"with {len(product_image_urls)} product images"
        )

        generation_tasks = [
            self.__generate_and_update_item(job, index, item, product_image_urls)
            for index, item in enumerate(plan_items)
        ]
        await asyncio.gather(*generation_tasks, return_exceptions=False)

        final_job = await campaign_generation_job_service.get(
            self.session_factory,
            job.id,
        )
        if not final_job.result:
            raise ValueError("Final job result not found")
        return final_job.result

    async def __generate_and_update_item(
        self,
        job: CampaignGenerationJob,
        item_index: int,
        item: ContentPlanItem,
        product_image_urls: list[str],
    ) -> None:
        try:
            product_image_url = self.__select_product_image(
                product_image_urls, item_index
            )

            result = await self.text_with_single_image_service.generate_full(
                brand_id=job.brand_id,
                channel=item.channel,
                image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE_IMAGE,
                caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
                user_prompt=format_as_xml(item),
                image_url=product_image_url,
            )

            update_request = ContentPlanItemUpdateRequest(
                content_data=TextWithSingleImageContentData(
                    caption=result.text,
                    image_url=result.image_url,
                ),
                image_urls=[result.image_url],
                status=JobStatus.COMPLETED,
            )
            logger.info(f"Product lifestyle item {item.id} completed")
        except Exception as e:
            logger.error(f"Failed to generate item {item.id}: {e}")
            update_request = ContentPlanItemUpdateRequest(
                status=JobStatus.FAILED,
            )

        await campaign_generation_job_service.update_posting_plan_item(
            self.session_factory,
            job.id,
            item.id,
            update_request,
        )

    def __get_product_image_urls(self, job: CampaignGenerationJob) -> list[str]:
        if not job.user_input:
            return []
        image_urls = getattr(job.user_input, "image_urls", None)
        return image_urls if image_urls else []

    def __select_product_image(
        self, product_image_urls: list[str], item_index: int
    ) -> str | None:
        if not product_image_urls:
            return None
        return product_image_urls[item_index % len(product_image_urls)]
