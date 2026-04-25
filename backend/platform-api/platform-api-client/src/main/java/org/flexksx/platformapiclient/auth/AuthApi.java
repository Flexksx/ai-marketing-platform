package org.flexksx.platformapiclient.auth;

import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange("/auth")
public interface AuthApi {

  @PostExchange("/login")
  LoginResponse login(@RequestBody LoginRequest request);

  @PostExchange("/logout")
  void logout();
}
