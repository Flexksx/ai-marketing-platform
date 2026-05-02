import asyncio
import logging

import public
from fastapi import Depends
from pydantic_ai import format_as_xml

import src.brands.service as brand_service
import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.shared import TextWithSingleImageContentGenerator
from webapp_api_contract.brands import Brand
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentPlanItem,
)
from webapp_api_contract.content_plan_items import ContentPlanItemUpdateRequest
from webapp_api_contract.shared import JobStatus


logger = logging.getLogger(__name__)


@public.add
class UserImagesOnlyPostGenerationCampaignGenerationStep:
    def __init__(
        self,
        session_factory: DbSessionFactory = Depends(),
        text_with_single_image_generation_service: (
            TextWithSingleImageContentGenerator
        ) = Depends(),
    ):
        self.session_factory = session_factory
        self.text_with_single_image_generation_service = (
            text_with_single_image_generation_service
        )

    async def generate(self, job: CampaignGenerationJob) -> CampaignGenerationJobResult:
        if not job.result or not job.result.content_plan_items:
            raise ValueError("Content plan items not found")

        brand = await brand_service.get(self.session_factory, job.brand_id)
        plan_items = job.result.content_plan_items

        logger.info(f"Starting generation of {len(plan_items)} posts")

        caption_tasks = [
            self.__generate_and_update_item(job.id, item, brand) for item in plan_items
        ]
        await asyncio.gather(*caption_tasks, return_exceptions=False)

        final_job = await campaign_generation_job_service.get(
            self.session_factory,
            job.id,
        )
        if not final_job.result:
            raise ValueError("Final job result not found")
        return final_job.result

    async def __generate_and_update_item(
        self,
        job_id: str,
        item: ContentPlanItem,
        brand: Brand,
    ) -> None:
        try:
            image_url = item.image_urls[0] if item.image_urls else None
            if not image_url:
                raise ValueError(f"No image URL for item {item.id}")

            tws = self.text_with_single_image_generation_service
            caption = await tws.generate_caption_for_image(
                brand_id=brand.id,
                channel=item.channel,
                caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
                user_prompt=format_as_xml([item]),
                image_url=image_url,
            )

            update_request = ContentPlanItemUpdateRequest(
                content_data=TextWithSingleImageContentData(
                    caption=caption,
                    image_url=image_url,
                ),
                image_urls=[image_url],
                status=JobStatus.COMPLETED,
            )
            logger.info(f"Content generated for item {item.id}")
        except Exception as e:
            logger.error(f"Failed to generate caption for item {item.id}: {e}")
            update_request = ContentPlanItemUpdateRequest(
                status=JobStatus.FAILED,
            )

        await campaign_generation_job_service.update_posting_plan_item(
            self.session_factory,
            job_id,
            item.id,
            update_request,
        )
