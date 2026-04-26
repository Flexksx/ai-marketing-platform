package org.flexksx.platformapiclient.auth;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange("/auth")
@Tag(name = "Authentication", description = "Endpoints for user authentication and session management")
public interface AuthApi {

  @PostExchange("/login")
  @Operation(summary = "Login", description = "Authenticate a user and return a JWT token")
  LoginResponse login(@RequestBody LoginRequest request);

  @PostExchange("/register")
  @Operation(summary = "Register", description = "Create a new user account and return a JWT token")
  LoginResponse register(@RequestBody LoginRequest request);

  @PostExchange("/logout")
  @Operation(summary = "Logout", description = "Invalidate the current user session")
  void logout();
}
