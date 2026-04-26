package org.flexksx.platformapiclient.brand.content;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;

@HttpExchange("/brands/{brandId}/content-items")
@Tag(name = "Brand Content", description = "Endpoints for managing content items within a brand")
public interface BrandContentApi {

  @GetExchange
  @Operation(summary = "Search brand content", description = "Retrieve a list of content items for a specific brand")
  List<ContentItemResponse> search(@PathVariable String brandId);

  @GetExchange("/{id}")
  @Operation(summary = "Get brand content item", description = "Retrieve details of a specific content item by ID")
  ContentItemResponse get(@PathVariable String brandId, @PathVariable String id);
}
