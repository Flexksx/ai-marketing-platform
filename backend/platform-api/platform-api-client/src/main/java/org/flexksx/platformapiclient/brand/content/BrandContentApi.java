package org.flexksx.platformapiclient.brand.content;

import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;

@HttpExchange("/brands/{brandId}/content-items")
public interface BrandContentApi {

  @GetExchange
  List<ContentItemResponse> search(@PathVariable String brandId);

  @GetExchange("/{id}")
  ContentItemResponse get(@PathVariable String brandId, @PathVariable String id);
}
