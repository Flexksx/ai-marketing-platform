package org.flexksx.platformapiservice.brand.service;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.brand.persistence.BrandRepository;
import org.flexksx.platformapiservice.brand.persistence.BrandRowMapper;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class BrandService {

  private final BrandRepository brandRepository;
  private final BrandRowMapper brandRowMapper;

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
    return brandRowMapper.toDomain(brandRepository.save(brandRowMapper.toEntity(brand)));
  }

  public void delete(String id) {
    if (!brandRepository.existsById(id)) {
      throw new BrandNotFoundException(id);
    }
    brandRepository.deleteById(id);
  }
}
