package org.flexksx.platformapiclient.brand;

import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.DeleteExchange;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange("/brands")
public interface BrandApi {

  @GetExchange()
  List<BrandResponse> search();

  @GetExchange("/{id}")
  BrandResponse get(@PathVariable String id);

  @PostExchange()
  BrandResponse create(CreateBrandRequest request);

  @DeleteExchange("/{id}")
  void delete(@PathVariable String id);
}
