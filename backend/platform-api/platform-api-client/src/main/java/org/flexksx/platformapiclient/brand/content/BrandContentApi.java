package org.flexksx.platformapiclient.brand.content;

import org.flexksx.platformapiclient.brand.BrandApi;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;

@HttpExchange(BrandApi.URL_PATH_BASE + "/{brandId}" + BrandContentApi.URL_PATH_BASE)
public interface BrandContentApi {
  String URL_PATH_BASE = "content-items";

  @GetExchange()
  ContentItemResponse search(@PathVariable String brandId);

  @GetExchange("/{id}")
  ContentItemResponse get(@PathVariable String brandId, @PathVariable String id);
}
