from fastapi import APIRouter, Body, Depends, Path

import src.content_plan_item.service as content_plan_item_service
from src.auth_access import validate_brand_access
from src.content_plan_item.model import (
    ContentPlanItem,
    ContentPlanItemUpdateRequest,
    RestContentPlanItemUpdateRequest,
)


router = APIRouter(tags=["Brand Campaign Creation Content Plan Items"])


@router.put("/{content_plan_item_id}", response_model=ContentPlanItem)
async def update_content_plan_item(
    job_id: str = Path(...),
    content_plan_item_id: str = Path(...),
    request: RestContentPlanItemUpdateRequest = Body(...),  # noqa: B008
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
):
    domain_request = ContentPlanItemUpdateRequest.model_validate(
        request.model_dump(exclude_unset=True)
    )
    item = await content_plan_item_service.update(content_plan_item_id, domain_request)
    if item.job_id != job_id:
        return item
    return item


@router.delete("/{content_plan_item_id}", status_code=204)
async def remove_content_plan_item(
    job_id: str = Path(...),
    content_plan_item_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
):
    item = await content_plan_item_service.get(content_plan_item_id)
    if item.job_id != job_id:
        return
    await content_plan_item_service.remove(content_plan_item_id)
