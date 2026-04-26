package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Request object for creating a new brand")
public record CreateBrandRequest(
    @Schema(description = "Name of the brand") @JsonProperty("name") String name,
    @Schema(description = "URL to the brand's website") @JsonProperty("website_url")
        String websiteUrl) {}
