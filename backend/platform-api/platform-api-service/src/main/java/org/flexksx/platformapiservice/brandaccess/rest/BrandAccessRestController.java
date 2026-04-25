package org.flexksx.platformapiservice.brandaccess.rest;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiclient.brand.member.AddBrandMemberRequest;
import org.flexksx.platformapiclient.brand.member.BrandMemberApi;
import org.flexksx.platformapiclient.brand.member.BrandMemberResponse;
import org.flexksx.platformapiclient.brand.member.UpdateBrandMemberRoleRequest;
import org.flexksx.platformapiservice.auth.UserPrincipal;
import org.flexksx.platformapiservice.brandaccess.service.BrandAccessService;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class BrandAccessRestController implements BrandMemberApi {

  private final BrandAccessService brandAccessService;
  private final BrandAccessRestMapper brandAccessRestMapper;

  @Override
  public List<BrandMemberResponse> list(String brandId) {
    return brandAccessService.listMembers(brandId, currentUserId()).stream()
        .map(brandAccessRestMapper::toResponse)
        .toList();
  }

  @Override
  public BrandMemberResponse add(String brandId, AddBrandMemberRequest request) {
    return brandAccessRestMapper.toResponse(
        brandAccessService.addMember(
            brandId,
            request.email(),
            brandAccessRestMapper.toDomainRole(request.role()),
            currentUserId()));
  }

  @Override
  public void remove(String brandId, String userId) {
    brandAccessService.removeMember(brandId, userId, currentUserId());
  }

  @Override
  public BrandMemberResponse updateRole(
      String brandId, String userId, UpdateBrandMemberRoleRequest request) {
    return brandAccessRestMapper.toResponse(
        brandAccessService.updateRole(
            brandId, userId, brandAccessRestMapper.toDomainRole(request.role()), currentUserId()));
  }

  private String currentUserId() {
    UserPrincipal principal =
        (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    return principal.getId();
  }
}
