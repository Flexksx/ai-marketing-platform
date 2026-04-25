package org.flexksx.platformapiclient.brand.member;

import com.fasterxml.jackson.annotation.JsonProperty;

public record AddBrandMemberRequest(
    @JsonProperty("email") String email, @JsonProperty("role") BrandMemberRole role) {}
