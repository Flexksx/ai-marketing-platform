package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;

public record CreateBrandRequest(
    @JsonProperty("name") String name, @JsonProperty("website_url") String websiteUrl) {}
