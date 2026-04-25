package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;

public record BrandResponse(
    @JsonProperty("id") String id,
    @JsonProperty("name") String name,
    @JsonProperty("data") BrandDataResponse data) {}
