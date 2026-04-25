package org.flexksx.platformapiservice.user.rest;

import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiclient.user.ChangePasswordRequest;
import org.flexksx.platformapiclient.user.UpdateUserRequest;
import org.flexksx.platformapiclient.user.UserApi;
import org.flexksx.platformapiclient.user.UserResponse;
import org.flexksx.platformapiservice.auth.UserPrincipal;
import org.flexksx.platformapiservice.user.service.UserService;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class UserRestController implements UserApi {

  private final UserService userService;
  private final UserRestMapper userRestMapper;

  @Override
  public UserResponse getMe() {
    return userRestMapper.toResponse(userService.get(currentUserId()));
  }

  @Override
  public UserResponse updateMe(UpdateUserRequest request) {
    return userRestMapper.toResponse(userService.updateEmail(currentUserId(), request.email()));
  }

  @Override
  public void changePassword(ChangePasswordRequest request) {
    userService.changePassword(currentUserId(), request.oldPassword(), request.newPassword());
  }

  private String currentUserId() {
    UserPrincipal principal =
        (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    return principal.getId();
  }
}
