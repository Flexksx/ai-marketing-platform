import asyncio
import logging

from sqlalchemy import select
from sqlalchemy import update as sa_update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_manager import get_session
from lib.model import JobStatus
from lib.utils import new_id
from src.brand.entity import BrandRecord
from src.campaign_generation.entity import CampaignGenerationJobRecord
from src.campaign_generation.errors import (
    CampaignGenerationJobNotFoundException,
    OptimisticLockError,
    PostingPlanItemNotFoundException,
)
from src.campaign_generation.model import (
    CampaignCreationJobUpdateInput,
    CampaignGenerationJob,
    CampaignGenerationJobCreateRequest,
    CampaignGenerationJobResult,
    ContentPlanItem,
)


logger = logging.getLogger(__name__)

_MAX_LOCK_RETRIES = 5
_POSTING_PLAN_LOCK = asyncio.Lock()


async def create(
    request: CampaignGenerationJobCreateRequest,
) -> CampaignGenerationJob:
    async with get_session() as session:
        user_input_dict = request.user_input.model_dump(mode="json")
        user_input_dict["workflow_type"] = request.workflow_type

        logger.debug(
            f"Creating job with workflow_type: {request.workflow_type}, "
            f"user_input: {user_input_dict}"
        )

        record = CampaignGenerationJobRecord(
            id=new_id(),
            brand_id=request.brand_id,
            workflow_type=request.workflow_type,
            user_input=user_input_dict,
            status=JobStatus.PENDING,
            result={},
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)

        logger.debug(
            f"Job created with id: {record.id}, "
            f"workflow_type: {record.workflow_type}, "
            f"user_input: {record.user_input}"
        )

        return CampaignGenerationJob.model_validate(record)


async def update(
    job_id: str,
    request: CampaignCreationJobUpdateInput,
) -> CampaignGenerationJob:
    async with get_session() as session:
        record = await _get_by_id(session, job_id)
        old_version = record.version

        update_values = {
            "status": request.status,
            "version": old_version + 1,
        }
        if request.result:
            update_values["result"] = request.result.model_dump(mode="json")

        stmt_result: CursorResult = await session.execute(  # ty:ignore[invalid-assignment]
            sa_update(CampaignGenerationJobRecord)
            .where(
                CampaignGenerationJobRecord.id == job_id,
                CampaignGenerationJobRecord.version == old_version,
            )
            .values(**update_values)
        )

        if stmt_result.rowcount == 0:
            raise OptimisticLockError(
                f"Job {job_id} was updated by another process (version conflict)"
            )

        await session.commit()

    return await get(job_id)


async def get(job_id: str) -> CampaignGenerationJob:
    async with get_session() as session:
        record = await _get_by_id(session, job_id)
        return CampaignGenerationJob.model_validate(record)


async def exists_for_user(
    job_id: str,
    user_id: str,
) -> bool:
    async with get_session() as session:
        statement = (
            select(CampaignGenerationJobRecord)
            .join(BrandRecord, CampaignGenerationJobRecord.brand_id == BrandRecord.id)
            .filter(
                CampaignGenerationJobRecord.id == job_id,
                BrandRecord.user_id == user_id,
            )
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none() is not None


async def update_posting_plan_item(
    job_id: str,
    item_id: str,
    updated_item: ContentPlanItem,
) -> CampaignGenerationJob:
    async with _POSTING_PLAN_LOCK, get_session() as session:
        for _ in range(_MAX_LOCK_RETRIES):
            record = await _get_by_id(session, job_id)
            old_version = record.version

            result = CampaignGenerationJobResult.model_validate(record.result or {})
            item_index = next(
                (
                    i
                    for i, item in enumerate(result.content_plan_items)
                    if item.id == item_id
                ),
                None,
            )
            if item_index is None:
                raise PostingPlanItemNotFoundException(job_id, item_id)

            result.content_plan_items[item_index] = updated_item
            updated_result = result.model_dump(mode="json")

            stmt_result: CursorResult = await session.execute(  # ty:ignore[invalid-assignment]
                sa_update(CampaignGenerationJobRecord)
                .where(
                    CampaignGenerationJobRecord.id == job_id,
                    CampaignGenerationJobRecord.version == old_version,
                )
                .values(result=updated_result, version=old_version + 1)
            )

            if stmt_result.rowcount > 0:
                await session.commit()
                logger.debug(f"Updated posting plan item {item_id} for job {job_id}")
                break

            await session.rollback()
        else:
            raise OptimisticLockError(
                f"Job {job_id} posting plan item {item_id} could not be "
                f"updated after {_MAX_LOCK_RETRIES} attempts"
            )

    return await get(job_id)


async def _get_by_id(session: AsyncSession, job_id: str) -> CampaignGenerationJobRecord:
    statement = select(CampaignGenerationJobRecord).filter(
        CampaignGenerationJobRecord.id == job_id
    )
    result = await session.execute(statement)
    record = result.scalar_one_or_none()
    if not record:
        raise CampaignGenerationJobNotFoundException(job_id)
    return record
