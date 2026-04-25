package org.flexksx.platformapiclient.auth;

import com.fasterxml.jackson.annotation.JsonProperty;

public record LoginResponse(@JsonProperty("token") String token) {}
