package org.flexksx.platformapiclient.brand;

import java.util.List;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;

@HttpExchange
public interface BrandApi {
  String URL_PATH_BASE = "/brands";

  @GetExchange(URL_PATH_BASE)
  List<BrandResponse> search();
}
