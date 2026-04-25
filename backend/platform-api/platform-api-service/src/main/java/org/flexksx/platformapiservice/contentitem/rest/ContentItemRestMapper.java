package org.flexksx.platformapiservice.contentitem.rest;

import org.flexksx.platformapiclient.brand.content.ContentItemResponse;
import org.flexksx.platformapiservice.contentitem.service.ContentItem;
import org.springframework.stereotype.Component;

@Component
public class ContentItemRestMapper {

  public ContentItemResponse toResponse(ContentItem contentItem) {
    return new ContentItemResponse(contentItem.id());
  }
}
