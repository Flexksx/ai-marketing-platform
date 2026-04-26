package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Response object containing brand information")
public record BrandResponse(
    @Schema(description = "Brand's unique identifier") @JsonProperty("id") String id,
    @Schema(description = "Brand's name") @JsonProperty("name") String name,
    @Schema(description = "Brand's metadata and configuration") @JsonProperty("data")
        BrandDataResponse data) {}
