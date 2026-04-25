package org.flexksx.platformapiclient.user;

import com.fasterxml.jackson.annotation.JsonProperty;

public record ChangePasswordRequest(
    @JsonProperty("old_password") String oldPassword,
    @JsonProperty("new_password") String newPassword) {}
