package org.flexksx.platformapiservice.brandaccess.rest;

import org.flexksx.platformapiclient.brand.member.BrandMemberResponse;
import org.flexksx.platformapiservice.brandaccess.service.BrandMember;
import org.flexksx.platformapiservice.brandaccess.service.BrandMemberRole;
import org.springframework.stereotype.Component;

@Component
public class BrandAccessRestMapper {

  public BrandMemberResponse toResponse(BrandMember member) {
    return new BrandMemberResponse(member.userId(), member.email(), toClientRole(member.role()));
  }

  public BrandMemberRole toDomainRole(
      org.flexksx.platformapiclient.brand.member.BrandMemberRole role) {
    return BrandMemberRole.valueOf(role.name());
  }

  private org.flexksx.platformapiclient.brand.member.BrandMemberRole toClientRole(
      BrandMemberRole role) {
    return org.flexksx.platformapiclient.brand.member.BrandMemberRole.valueOf(role.name());
  }
}
