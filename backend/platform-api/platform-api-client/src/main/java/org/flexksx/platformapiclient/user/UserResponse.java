package org.flexksx.platformapiclient.user;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Response object containing user profile information")
public record UserResponse(
    @Schema(description = "User's unique identifier") @JsonProperty("id") String id,
    @Schema(description = "User's email address") @JsonProperty("email") String email) {}
