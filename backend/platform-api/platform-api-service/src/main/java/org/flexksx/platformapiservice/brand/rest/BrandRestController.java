package org.flexksx.platformapiservice.brand.rest;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiclient.brand.BrandApi;
import org.flexksx.platformapiclient.brand.BrandResponse;
import org.flexksx.platformapiclient.brand.CreateBrandRequest;
import org.flexksx.platformapiservice.auth.UserPrincipal;
import org.flexksx.platformapiservice.brand.service.Brand;
import org.flexksx.platformapiservice.brand.service.BrandService;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class BrandRestController implements BrandApi {

  private final BrandService brandService;
  private final BrandRestMapper brandRestMapper;

  @Override
  public List<BrandResponse> search() {
    return brandService.search(currentUserId()).stream().map(brandRestMapper::toResponse).toList();
  }

  @Override
  public BrandResponse get(String id) {
    Brand brand = brandService.get(id, currentUserId());
    return brandRestMapper.toResponse(brand);
  }

  @Override
  public BrandResponse create(CreateBrandRequest request) {
    Brand brand = brandRestMapper.toDomain(request);
    Brand created = brandService.create(brand, currentUserId());
    return brandRestMapper.toResponse(created);
  }

  @Override
  public void delete(String id) {
    brandService.delete(id, currentUserId());
  }

  private String currentUserId() {
    UserPrincipal principal =
        (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    return principal.getId();
  }
}
