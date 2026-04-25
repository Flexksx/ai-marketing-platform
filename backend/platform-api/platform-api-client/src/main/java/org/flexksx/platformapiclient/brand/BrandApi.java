package org.flexksx.platformapiclient.brand;

import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.DeleteExchange;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange(BrandApi.URL_PATH_BASE)
public interface BrandApi {
  String URL_PATH_BASE = "/brands";

  @GetExchange(URL_PATH_BASE)
  List<BrandResponse> search();

  @GetExchange(URL_PATH_BASE + "/{id}")
  BrandResponse get(@PathVariable String id);

  @PostExchange(URL_PATH_BASE)
  BrandResponse create(CreateBrandRequest request);

  @DeleteExchange(URL_PATH_BASE + "/{id}")
  void delete(@PathVariable String id);
}
