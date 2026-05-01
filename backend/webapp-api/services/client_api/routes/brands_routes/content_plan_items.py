from fastapi import APIRouter, Body, Depends, Path

from services.client_api.auth.access_validation import validate_brand_access
from aimarketing.domain.content_plan_item import (
    ContentPlanItem,
    ContentPlanItemService,
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
    service: ContentPlanItemService = Depends(),
):
    domain_request = ContentPlanItemUpdateRequest.model_validate(
        request.model_dump(exclude_unset=True)
    )
    item = await service.update(content_plan_item_id, domain_request)
    if item.job_id != job_id:
        return item
    return item


@router.delete(
    "/{content_plan_item_id}",
    status_code=204,
)
async def remove_content_plan_item(
    job_id: str = Path(...),
    content_plan_item_id: str = Path(...),
    brand_id: str = Depends(validate_brand_access),  # noqa: ARG001
    service: ContentPlanItemService = Depends(),
):
    item = await service.get(content_plan_item_id)
    if item.job_id != job_id:
        return
    await service.remove(content_plan_item_id)
