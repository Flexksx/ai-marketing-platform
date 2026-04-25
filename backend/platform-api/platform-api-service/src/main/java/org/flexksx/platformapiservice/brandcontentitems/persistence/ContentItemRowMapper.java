package org.flexksx.platformapiservice.brandcontentitems.persistence;

import org.flexksx.platformapiservice.brandcontentitems.service.ContentItem;
import org.springframework.stereotype.Component;

@Component
public class ContentItemRowMapper {

  public ContentItem toDomain(ContentItemEntity entity) {
    return new ContentItem(entity.getId(), entity.getBrandId());
  }

  public ContentItemEntity toEntity(ContentItem contentItem) {
    return new ContentItemEntity(contentItem.id(), contentItem.brandId());
  }
}
