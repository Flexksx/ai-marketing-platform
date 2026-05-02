import asyncio
import logging

import public
from fastapi import Depends
from pydantic_ai import format_as_xml

import src.campaign_generation.service as campaign_generation_job_service
from lib.db.session_factory import DbSessionFactory
from lib.prompts import PromptTemplateName
from src.shared.text_with_single_image import (
    TextWithSingleImageContentGenerator,
)
from webapp_api_contract.campaign_generation import (
    CampaignGenerationJob,
    CampaignGenerationJobResult,
    ContentPlanItem,
)
from webapp_api_contract.content import TextWithSingleImageContentData
from webapp_api_contract.content_plan_items import ContentPlanItemUpdateRequest
from webapp_api_contract.shared import JobStatus


logger = logging.getLogger(__name__)


@public.add
class AIGeneratedCampaignContentGenerator:
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
        logger.info(f"Generating {len(plan_items)} posts using AI")

        generation_tasks = [
            self.__generate_and_update_item(job, item) for item in plan_items
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
        item: ContentPlanItem,
    ) -> None:
        try:
            result = await self.text_with_single_image_service.generate_full(
                brand_id=job.brand_id,
                channel=item.channel,
                image_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED_IMAGE,
                caption_prompt_template_name=PromptTemplateName.TEXT_WITH_SINGLE_IMAGE_CAPTION,
                user_prompt=format_as_xml(item),
                image_url=None,
            )
            update_request = ContentPlanItemUpdateRequest(
                content_data=TextWithSingleImageContentData(
                    caption=result.text,
                    image_url=result.image_url,
                ),
                image_urls=[result.image_url],
                status=JobStatus.COMPLETED,
            )
            await campaign_generation_job_service.update_posting_plan_item(
                self.session_factory,
                job.id,
                item.id,
                update_request,
            )
            logger.info(f"Item {item.id} completed")
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
