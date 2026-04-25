package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;

public record BrandDataResponse(
    @JsonProperty("logo_url") String logoUrl, @JsonProperty("website_url") String websiteUrl) {}
