package org.flexksx.platformapiclient.brand.member;

import com.fasterxml.jackson.annotation.JsonProperty;

public record UpdateBrandMemberRoleRequest(@JsonProperty("role") BrandMemberRole role) {}
