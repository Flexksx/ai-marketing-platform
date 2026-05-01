import asyncio
import logging

import httpx
from fastapi import Depends
from google.cloud import tasks_v2
from pydantic import BaseModel

from aimarketing.config import Settings, get_settings
from aimarketing.lib.cloudtasks.schema import (
    BrandGenerationTaskPayload,
    CampaignGenerationTaskPayload,
    ContentGenerationTaskPayload,
    PostGenerationTaskPayload,
)


logger = logging.getLogger(__name__)


class CloudTasksService:
    def __init__(
        self,
        settings: Settings = Depends(get_settings),
    ):
        self.project_id = settings.gcp_project_id
        self.location = settings.gcp_location
        self.queue_name = settings.cloud_tasks_queue
        self.worker_url = settings.worker_service_url.rstrip("/")
        self.environment = settings.environment
        self.service_account_email = settings.worker_service_account_email

        if self.is_production:
            self.client = tasks_v2.CloudTasksClient()
            self.parent = self.client.queue_path(
                self.project_id, self.location, self.queue_name
            )
        else:
            self.client = None
            self.parent = None

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    async def enqueue_campaign_generation(self, job_id: str, user_id: str):
        payload = CampaignGenerationTaskPayload(job_id=job_id, user_id=user_id)
        await self._enqueue(relative_url="/tasks/campaign-generation", payload=payload)

    async def enqueue_brand_generation(self, job_id: str):
        payload = BrandGenerationTaskPayload(job_id=job_id)
        await self._enqueue(relative_url="/tasks/brand-generation", payload=payload)

    async def enqueue_content_generation(self, job_id: str):
        payload = ContentGenerationTaskPayload(job_id=job_id)
        await self._enqueue(relative_url="/tasks/content-generation", payload=payload)

    async def enqueue_post_generation(
        self,
        job_id: str,
        user_id: str,
        brand_brief: str,
        campaign_brief: str,
        channel: str,
        topic: str,
        image_url: str,
        scheduled_at: str,
    ):
        payload = PostGenerationTaskPayload(
            job_id=job_id,
            user_id=user_id,
            brand_brief=brand_brief,
            campaign_brief=campaign_brief,
            channel=channel,
            topic=topic,
            image_url=image_url,
            scheduled_at=scheduled_at,
        )

        await self._enqueue(relative_url="/tasks/post-generation", payload=payload)

    async def _enqueue(self, relative_url: str, payload: BaseModel) -> None:
        target_url = f"{self.worker_url}{relative_url}"

        if self.is_production:
            await self._dispatch_to_google_cloud(target_url, payload)
        else:
            await self._dispatch_to_local_worker(target_url, payload)

    async def _dispatch_to_google_cloud(self, url: str, payload: BaseModel):
        """
        Creates a Cloud Task with OIDC Authentication.
        """
        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url,
                "headers": {"Content-Type": "application/json"},
                "body": payload.model_dump_json().encode(),
            }
        }

        if self.service_account_email:
            task["http_request"]["oidc_token"] = {
                "service_account_email": self.service_account_email,
                "audience": self.worker_url,
            }
        else:
            logger.warning(
                "⚠️ No Service Account Email provided! Cloud Task might fail 403 Forbidden."
            )

        try:
            if not self.client:
                raise ValueError("Client is not initialized")

            # CloudTasksClient is synchronous, so we run it in a thread to not block FastAPI
            response = await asyncio.to_thread(
                self.client.create_task,
                request={"parent": self.parent, "task": task},
            )
            logger.info(f"☁️  Cloud Task Created: {response.name} -> {url}")

        except Exception as e:
            logger.error(f"❌ Failed to create Cloud Task: {e}", exc_info=True)
            raise e

    async def _dispatch_to_local_worker(self, url: str, payload: BaseModel):
        logger.info(f"Dispatching local task to {url}")
        asyncio.create_task(
            self._send_local_request(url, payload.model_dump(mode="json"))
        )

    async def _send_local_request(self, url: str, json_payload: dict):
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(
                    url, json=json_payload, headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                logger.info(f"✅ Local task finished successfully: {url}")
        except Exception as e:
            logger.error(f"❌ Local task failed for {url}: {e}")
