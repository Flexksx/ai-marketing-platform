package org.flexksx.platformapiservice.brand.rest;

import java.util.List;
import org.flexksx.platformapiclient.brand.BrandApi;
import org.flexksx.platformapiclient.brand.BrandResponse;
import org.flexksx.platformapiclient.brand.CreateBrandRequest;
import org.flexksx.platformapiservice.brand.service.Brand;
import org.flexksx.platformapiservice.brand.service.BrandService;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BrandRestController implements BrandApi {

  private final BrandService brandService;
  private final BrandRestMapper brandRestMapper;

  public BrandRestController(BrandService brandService, BrandRestMapper brandRestMapper) {
    this.brandService = brandService;
    this.brandRestMapper = brandRestMapper;
  }

  @Override
  public List<BrandResponse> search() {
    return brandService.search().stream().map(brandRestMapper::toResponse).toList();
  }

  @Override
  public BrandResponse get(String id) {
    Brand brand = brandService.get(id);
    return brandRestMapper.toResponse(brand);
  }

  @Override
  public BrandResponse create(CreateBrandRequest request) {
    Brand brand = brandRestMapper.toDomain(request);
    Brand created = brandService.create(brand);
    return brandRestMapper.toResponse(created);
  }

  @Override
  public void delete(String id) {
    brandService.delete(id);
  }
}
