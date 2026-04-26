package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Response object containing brand metadata")
public record BrandDataResponse(
    @Schema(description = "URL to the brand's logo") @JsonProperty("logo_url") String logoUrl,
    @Schema(description = "URL to the brand's website") @JsonProperty("website_url")
        String websiteUrl) {}
