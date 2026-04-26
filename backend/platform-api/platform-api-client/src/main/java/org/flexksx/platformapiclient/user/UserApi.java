package org.flexksx.platformapiclient.user;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PatchExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange("/users")
@Tag(name = "Users", description = "Endpoints for user profile management")
public interface UserApi {

  @GetExchange("/me")
  @Operation(
      summary = "Get current user",
      description = "Retrieve the profile of the currently authenticated user")
  UserResponse getMe();

  @PatchExchange("/me")
  @Operation(
      summary = "Update current user",
      description = "Update the profile of the currently authenticated user")
  UserResponse updateMe(@RequestBody UpdateUserRequest request);

  @PostExchange("/me/password")
  @Operation(
      summary = "Change password",
      description = "Change the password of the currently authenticated user")
  void changePassword(@RequestBody ChangePasswordRequest request);
}
