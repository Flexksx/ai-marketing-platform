package org.flexksx.platformapiclient.brand.member;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Request object for adding a new member to a brand")
public record AddBrandMemberRequest(
    @Schema(description = "Email address of the user to add") @JsonProperty("email") String email,
    @Schema(description = "Role to assign to the new member") @JsonProperty("role")
        BrandMemberRole role) {}
