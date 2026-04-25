package org.flexksx.platformapiservice.brandcontentitems.rest;

import java.util.List;
import org.flexksx.platformapiclient.brand.content.BrandContentApi;
import org.flexksx.platformapiclient.brand.content.ContentItemResponse;
import org.flexksx.platformapiservice.brandcontentitems.service.ContentItem;
import org.flexksx.platformapiservice.brandcontentitems.service.ContentItemService;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BrandContentItemsRestController implements BrandContentApi {

  private final ContentItemService contentItemService;
  private final ContentItemRestMapper contentItemRestMapper;

  public BrandContentItemsRestController(
      ContentItemService contentItemService, ContentItemRestMapper contentItemRestMapper) {
    this.contentItemService = contentItemService;
    this.contentItemRestMapper = contentItemRestMapper;
  }

  @Override
  public List<ContentItemResponse> search(String brandId) {
    return contentItemService.searchByBrand(brandId).stream()
        .map(contentItemRestMapper::toResponse)
        .toList();
  }

  @Override
  public ContentItemResponse get(String brandId, String id) {
    ContentItem contentItem = contentItemService.get(id, brandId);
    return contentItemRestMapper.toResponse(contentItem);
  }
}
