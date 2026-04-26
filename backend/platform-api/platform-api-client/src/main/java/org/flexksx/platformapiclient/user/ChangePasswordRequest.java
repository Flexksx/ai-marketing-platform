package org.flexksx.platformapiclient.user;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Request object for changing user password")
public record ChangePasswordRequest(
    @Schema(description = "Current password") @JsonProperty("old_password") String oldPassword,
    @Schema(description = "New password") @JsonProperty("new_password") String newPassword) {}
