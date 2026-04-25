package org.flexksx.platformapiservice.brandaccess.service;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.brand.service.BrandService;
import org.flexksx.platformapiservice.brandaccess.persistence.BrandAccessEntity;
import org.flexksx.platformapiservice.brandaccess.persistence.BrandAccessRepository;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.flexksx.platformapiservice.user.persistence.UserRepository;
import org.flexksx.platformapiservice.user.service.UserNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class BrandAccessService {

  private final BrandAccessRepository brandAccessRepository;
  private final UserRepository userRepository;
  private final BrandService brandService;

  public List<BrandMember> listMembers(String brandId, String requestingUserId) {
    // Verify the requester has access to this brand
    brandService.get(brandId, requestingUserId);
    return brandAccessRepository.findAllByBrandId(brandId).stream().map(this::toMember).toList();
  }

  @Transactional
  public BrandMember addMember(
      String brandId, String email, BrandMemberRole role, String requestingUserId) {
    brandService.get(brandId, requestingUserId);
    UserEntity user =
        userRepository.findByEmail(email).orElseThrow(() -> new UserNotFoundException(email));
    if (brandAccessRepository.existsByUserIdAndBrandId(user.getId(), brandId)) {
      throw new BrandMemberAlreadyExistsException(user.getId(), brandId);
    }
    BrandAccessEntity saved =
        brandAccessRepository.save(BrandAccessEntity.of(user.getId(), brandId, role));
    return toMember(saved, user);
  }

  @Transactional
  public void removeMember(String brandId, String userId, String requestingUserId) {
    brandService.get(brandId, requestingUserId);
    BrandAccessEntity membership =
        brandAccessRepository
            .findByUserIdAndBrandId(userId, brandId)
            .orElseThrow(() -> new BrandMemberNotFoundException(userId, brandId));
    brandAccessRepository.delete(membership);
  }

  @Transactional
  public BrandMember updateRole(
      String brandId, String userId, BrandMemberRole role, String requestingUserId) {
    brandService.get(brandId, requestingUserId);
    BrandAccessEntity membership =
        brandAccessRepository
            .findByUserIdAndBrandId(userId, brandId)
            .orElseThrow(() -> new BrandMemberNotFoundException(userId, brandId));
    membership.setRole(role);
    BrandAccessEntity saved = brandAccessRepository.save(membership);
    return toMember(saved);
  }

  private BrandMember toMember(BrandAccessEntity entity) {
    UserEntity user =
        userRepository
            .findById(entity.getUserId())
            .orElseThrow(() -> new UserNotFoundException(entity.getUserId()));
    return toMember(entity, user);
  }

  private BrandMember toMember(BrandAccessEntity entity, UserEntity user) {
    return new BrandMember(user.getId(), user.getEmail(), entity.getRole());
  }
}
