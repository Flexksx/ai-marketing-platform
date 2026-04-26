package org.flexksx.platformapiclient.brand.member;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Request object for updating a brand member's role")
public record UpdateBrandMemberRoleRequest(
    @Schema(description = "New role to assign to the member") @JsonProperty("role")
        BrandMemberRole role) {}
