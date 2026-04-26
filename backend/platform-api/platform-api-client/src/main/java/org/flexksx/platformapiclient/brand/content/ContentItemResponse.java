package org.flexksx.platformapiclient.brand.content;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Response object containing content item information")
public record ContentItemResponse(
    @Schema(description = "Content item's unique identifier") @JsonProperty("id") String id) {}
