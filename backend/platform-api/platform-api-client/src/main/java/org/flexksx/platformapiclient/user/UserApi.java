package org.flexksx.platformapiclient.user;

import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PatchExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange("/users")
public interface UserApi {

  @GetExchange("/me")
  UserResponse getMe();

  @PatchExchange("/me")
  UserResponse updateMe(@RequestBody UpdateUserRequest request);

  @PostExchange("/me/password")
  void changePassword(@RequestBody ChangePasswordRequest request);
}
