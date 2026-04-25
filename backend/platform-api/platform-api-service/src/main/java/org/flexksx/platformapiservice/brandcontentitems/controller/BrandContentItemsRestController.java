package org.flexksx.platformapiservice.brandcontentitems.controller;

import java.util.List;
import org.flexksx.platformapiclient.brand.content.BrandContentApi;
import org.flexksx.platformapiclient.brand.content.ContentItemResponse;
import org.flexksx.platformapiservice.brandcontentitems.domain.ContentItem;
import org.flexksx.platformapiservice.brandcontentitems.domain.ContentItemService;
import org.flexksx.platformapiservice.brandcontentitems.mapper.ContentItemRestMapper;
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
