package org.flexksx.platformapiclient.brand.member;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Roles available for brand members")
public enum BrandMemberRole {
  @Schema(description = "Full administrative access to the brand")
  OWNER,
  @Schema(description = "Regular member access to the brand")
  MEMBER
}
