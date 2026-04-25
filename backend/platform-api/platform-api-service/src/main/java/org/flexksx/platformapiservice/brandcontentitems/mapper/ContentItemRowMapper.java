package org.flexksx.platformapiservice.brandcontentitems.mapper;

import org.flexksx.platformapiservice.brandcontentitems.domain.ContentItem;
import org.flexksx.platformapiservice.brandcontentitems.persistence.ContentItemEntity;
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
