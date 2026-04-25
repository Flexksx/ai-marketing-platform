package org.flexksx.platformapiservice.contentitem.rest;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiclient.brand.content.BrandContentApi;
import org.flexksx.platformapiclient.brand.content.ContentItemResponse;
import org.flexksx.platformapiservice.contentitem.service.ContentItem;
import org.flexksx.platformapiservice.contentitem.service.ContentItemService;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class BrandContentItemsRestController implements BrandContentApi {

  private final ContentItemService contentItemService;
  private final ContentItemRestMapper contentItemRestMapper;

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
