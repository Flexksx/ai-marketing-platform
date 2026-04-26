package org.flexksx.platformapiservice.auth;

import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiclient.auth.AuthApi;
import org.flexksx.platformapiclient.auth.LoginRequest;
import org.flexksx.platformapiclient.auth.LoginResponse;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class AuthRestController implements AuthApi {

  private final AuthService authService;

  @Override
  public LoginResponse login(LoginRequest request) {
    String token = authService.login(request.email(), request.password());
    return new LoginResponse(token);
  }

  @Override
  public LoginResponse register(LoginRequest request) {
    String token = authService.register(request.email(), request.password());
    return new LoginResponse(token);
  }

  @Override
  public void logout() {
    UserPrincipal principal =
        (UserPrincipal) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
    authService.logout(principal.getId());
  }
}
