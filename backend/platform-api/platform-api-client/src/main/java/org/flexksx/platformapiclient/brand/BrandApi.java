package org.flexksx.platformapiclient.brand;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.DeleteExchange;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange("/brands")
@Tag(name = "Brands", description = "Endpoints for brand management")
public interface BrandApi {

  @GetExchange()
  @Operation(
      summary = "Search brands",
      description = "Retrieve a list of brands the user has access to")
  List<BrandResponse> search();

  @GetExchange("/{id}")
  @Operation(summary = "Get brand", description = "Retrieve details of a specific brand by ID")
  BrandResponse get(@PathVariable String id);

  @PostExchange()
  @Operation(summary = "Create brand", description = "Create a new brand")
  BrandResponse create(@RequestBody CreateBrandRequest request);

  @DeleteExchange("/{id}")
  @Operation(summary = "Delete brand", description = "Delete a specific brand by ID")
  void delete(@PathVariable String id);
}
