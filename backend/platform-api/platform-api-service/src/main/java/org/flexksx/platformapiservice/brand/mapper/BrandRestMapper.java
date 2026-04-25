package org.flexksx.platformapiservice.brand.mapper;

import org.flexksx.platformapiclient.brand.BrandDataResponse;
import org.flexksx.platformapiclient.brand.BrandResponse;
import org.flexksx.platformapiclient.brand.CreateBrandRequest;
import org.flexksx.platformapiservice.brand.domain.Brand;
import org.flexksx.platformapiservice.brand.domain.BrandData;
import org.springframework.stereotype.Component;

@Component
public class BrandRestMapper {

  public BrandResponse toResponse(Brand brand) {
    BrandDataResponse dataResponse =
        new BrandDataResponse(brand.data().logoUrl(), brand.data().websiteUrl());
    return new BrandResponse(brand.id(), brand.name(), dataResponse);
  }

  public Brand toDomain(CreateBrandRequest request) {
    BrandData data = new BrandData(null, request.websiteUrl());
    return new Brand(null, request.name(), data);
  }
}
