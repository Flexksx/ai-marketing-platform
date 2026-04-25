package org.flexksx.platformapiservice.brand.service;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.brand.persistence.BrandEntity;
import org.flexksx.platformapiservice.brand.persistence.BrandRepository;
import org.flexksx.platformapiservice.brand.persistence.BrandRowMapper;
import org.flexksx.platformapiservice.brandaccess.persistence.BrandAccessEntity;
import org.flexksx.platformapiservice.brandaccess.persistence.BrandAccessRepository;
import org.flexksx.platformapiservice.brandaccess.service.BrandMemberRole;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class BrandService {

  private final BrandRepository brandRepository;
  private final BrandRowMapper brandRowMapper;
  private final BrandAccessRepository brandAccessRepository;

  public List<Brand> search(String userId) {
    return brandRepository.findAllByUserId(userId).stream().map(brandRowMapper::toDomain).toList();
  }

  public Brand get(String id, String userId) {
    return brandRepository
        .findByIdAndUserId(id, userId)
        .map(brandRowMapper::toDomain)
        .orElseThrow(() -> new BrandNotFoundException(id));
  }

  @Transactional
  public Brand create(Brand brand, String userId) {
    BrandEntity saved = brandRepository.save(brandRowMapper.toEntity(brand));
    brandAccessRepository.save(BrandAccessEntity.of(userId, saved.getId(), BrandMemberRole.OWNER));
    return brandRowMapper.toDomain(saved);
  }

  public void delete(String id, String userId) {
    brandRepository.findByIdAndUserId(id, userId).orElseThrow(() -> new BrandNotFoundException(id));
    brandRepository.deleteById(id);
  }
}
