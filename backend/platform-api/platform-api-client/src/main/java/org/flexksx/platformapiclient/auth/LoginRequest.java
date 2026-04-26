package org.flexksx.platformapiclient.auth;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Request object for user login")
public record LoginRequest(
    @Schema(description = "User's email address", example = "user@example.com")
        @JsonProperty("email")
        String email,
    @Schema(description = "User's password") @JsonProperty("password") String password) {}
