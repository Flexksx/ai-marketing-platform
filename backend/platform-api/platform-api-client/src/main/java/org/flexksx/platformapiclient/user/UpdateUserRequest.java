package org.flexksx.platformapiclient.user;

import com.fasterxml.jackson.annotation.JsonProperty;

public record UpdateUserRequest(@JsonProperty("email") String email) {}
