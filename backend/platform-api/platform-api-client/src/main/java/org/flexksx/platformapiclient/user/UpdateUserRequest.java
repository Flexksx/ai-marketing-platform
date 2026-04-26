package org.flexksx.platformapiclient.user;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Request object for updating user profile")
public record UpdateUserRequest(
    @Schema(description = "New email address for the user") @JsonProperty("email") String email) {}
