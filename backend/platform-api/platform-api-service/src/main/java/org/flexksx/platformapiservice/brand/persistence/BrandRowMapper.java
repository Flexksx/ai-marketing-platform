package org.flexksx.platformapiservice.brand.persistence;

import org.flexksx.platformapiservice.brand.service.Brand;
import org.flexksx.platformapiservice.brand.service.BrandData;
import org.springframework.stereotype.Component;

@Component
public class BrandRowMapper {

  public Brand toDomain(BrandEntity entity) {
    BrandData data = new BrandData(entity.getLogoUrl(), entity.getWebsiteUrl());
    return new Brand(entity.getId(), entity.getName(), data);
  }

  public BrandEntity toEntity(Brand brand) {
    String logoUrl = brand.data() != null ? brand.data().logoUrl() : null;
    String websiteUrl = brand.data() != null ? brand.data().websiteUrl() : null;
    return new BrandEntity(brand.id(), brand.name(), logoUrl, websiteUrl);
  }
}
