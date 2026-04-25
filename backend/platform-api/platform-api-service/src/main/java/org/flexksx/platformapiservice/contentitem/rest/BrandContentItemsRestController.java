package org.flexksx.platformapiservice.contentitem.rest;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiclient.brand.content.BrandContentApi;
import org.flexksx.platformapiclient.brand.content.ContentItemResponse;
import org.flexksx.platformapiservice.auth.UserPrincipal;
import org.flexksx.platformapiservice.brand.service.BrandService;
import org.flexksx.platformapiservice.contentitem.service.ContentItem;
import org.flexksx.platformapiservice.contentitem.service.ContentItemService;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class BrandContentItemsRestController implements BrandContentApi {

  private final ContentItemService contentItemService;
  private final ContentItemRestMapper contentItemRestMapper;
  private final BrandService brandService;

  @Override
  public List<ContentItemResponse> search(String brandId) {
    brandService.get(brandId, currentUserId());
    return contentItemService.searchByBrand(brandId).stream()
        .map(contentItemRestMapper::toResponse)
        .toList();
  }

  @Override
  public ContentItemResponse get(String brandId, String id) {
    brandService.get(brandId, currentUserId());
    ContentItem contentItem = contentItemService.get(id, brandId);
    return contentItemRestMapper.toResponse(contentItem);
  }

  private String currentUserId() {
    UserPrincipal principal =
        (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    return principal.getId();
  }
}
