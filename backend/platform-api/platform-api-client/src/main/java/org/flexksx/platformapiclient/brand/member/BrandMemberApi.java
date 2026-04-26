package org.flexksx.platformapiclient.brand.member;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.DeleteExchange;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;
import org.springframework.web.service.annotation.PutExchange;

@HttpExchange("/brands/{brandId}/members")
@Tag(name = "Brand Members", description = "Endpoints for managing brand members and their roles")
public interface BrandMemberApi {

  @GetExchange
  @Operation(
      summary = "List brand members",
      description = "Retrieve a list of members for a specific brand")
  List<BrandMemberResponse> list(@PathVariable String brandId);

  @PostExchange
  @Operation(summary = "Add brand member", description = "Add a new member to a specific brand")
  BrandMemberResponse add(@PathVariable String brandId, @RequestBody AddBrandMemberRequest request);

  @DeleteExchange("/{userId}")
  @Operation(summary = "Remove brand member", description = "Remove a member from a specific brand")
  void remove(@PathVariable String brandId, @PathVariable String userId);

  @PutExchange("/{userId}/role")
  @Operation(
      summary = "Update brand member role",
      description = "Update the role of a specific brand member")
  BrandMemberResponse updateRole(
      @PathVariable String brandId,
      @PathVariable String userId,
      @RequestBody UpdateBrandMemberRoleRequest request);
}
