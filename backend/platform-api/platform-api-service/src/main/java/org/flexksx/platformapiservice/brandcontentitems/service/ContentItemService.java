package org.flexksx.platformapiservice.brandcontentitems.service;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.brandcontentitems.persistence.ContentItemRepository;
import org.flexksx.platformapiservice.brandcontentitems.persistence.ContentItemRowMapper;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ContentItemService {

  private final ContentItemRepository contentItemRepository;
  private final ContentItemRowMapper contentItemRowMapper;

  public List<ContentItem> searchByBrand(String brandId) {
    return contentItemRepository.findAllByBrandId(brandId).stream()
        .map(contentItemRowMapper::toDomain)
        .toList();
  }

  public ContentItem get(String id, String brandId) {
    return contentItemRepository
        .findByIdAndBrandId(id, brandId)
        .map(contentItemRowMapper::toDomain)
        .orElseThrow(() -> new ContentItemNotFoundException(id, brandId));
  }
}
