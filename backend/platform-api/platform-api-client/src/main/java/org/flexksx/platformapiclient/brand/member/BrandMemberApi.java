package org.flexksx.platformapiclient.brand.member;

import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.DeleteExchange;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;
import org.springframework.web.service.annotation.PutExchange;

@HttpExchange("/brands/{brandId}/members")
public interface BrandMemberApi {

  @GetExchange
  List<BrandMemberResponse> list(@PathVariable String brandId);

  @PostExchange
  BrandMemberResponse add(@PathVariable String brandId, @RequestBody AddBrandMemberRequest request);

  @DeleteExchange("/{userId}")
  void remove(@PathVariable String brandId, @PathVariable String userId);

  @PutExchange("/{userId}/role")
  BrandMemberResponse updateRole(
      @PathVariable String brandId,
      @PathVariable String userId,
      @RequestBody UpdateBrandMemberRoleRequest request);
}
