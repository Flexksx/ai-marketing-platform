package org.flexksx.platformapiclient.brand.member;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Response object containing brand member information")
public record BrandMemberResponse(
    @Schema(description = "Member's unique user identifier") @JsonProperty("user_id") String userId,
    @Schema(description = "Member's email address") @JsonProperty("email") String email,
    @Schema(description = "Member's role within the brand") @JsonProperty("role")
        BrandMemberRole role) {}
