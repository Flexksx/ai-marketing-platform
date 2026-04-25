package org.flexksx.platformapiservice.brand.domain;

import java.util.List;
import org.flexksx.platformapiservice.brand.mapper.BrandRowMapper;
import org.flexksx.platformapiservice.brand.persistence.BrandEntity;
import org.flexksx.platformapiservice.brand.persistence.BrandRepository;
import org.springframework.stereotype.Service;

@Service
public class BrandService {

  private final BrandRepository brandRepository;
  private final BrandRowMapper brandRowMapper;

  public BrandService(BrandRepository brandRepository, BrandRowMapper brandRowMapper) {
    this.brandRepository = brandRepository;
    this.brandRowMapper = brandRowMapper;
  }

  public List<Brand> search() {
    return brandRepository.findAll().stream().map(brandRowMapper::toDomain).toList();
  }

  public Brand get(String id) {
    return brandRepository
        .findById(id)
        .map(brandRowMapper::toDomain)
        .orElseThrow(() -> new BrandNotFoundException(id));
  }

  public Brand create(Brand brand) {
    BrandEntity entity = brandRowMapper.toEntity(brand);
    BrandEntity saved = brandRepository.save(entity);
    return brandRowMapper.toDomain(saved);
  }

  public void delete(String id) {
    if (!brandRepository.existsById(id)) {
      throw new BrandNotFoundException(id);
    }
    brandRepository.deleteById(id);
  }
}
