package org.flexksx.platformapiclient.brand.member;

import com.fasterxml.jackson.annotation.JsonProperty;

public record BrandMemberResponse(
    @JsonProperty("user_id") String userId,
    @JsonProperty("email") String email,
    @JsonProperty("role") BrandMemberRole role) {}
