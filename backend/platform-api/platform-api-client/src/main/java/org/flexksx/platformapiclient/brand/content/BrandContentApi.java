package org.flexksx.platformapiclient.brand.content;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;

@HttpExchange("brands/{brandId}/content-items")
public interface BrandContentApi {

  @GetExchange
  ContentItemResponse search(@PathVariable String brandId);

  @GetExchange("/{id}")
  ContentItemResponse get(@PathVariable String brandId, @PathVariable String id);
}
