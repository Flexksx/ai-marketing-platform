package org.flexksx.platformapiclient.auth;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Response object containing the authentication token")
public record LoginResponse(
    @Schema(description = "JWT authentication token") @JsonProperty("token") String token) {}
