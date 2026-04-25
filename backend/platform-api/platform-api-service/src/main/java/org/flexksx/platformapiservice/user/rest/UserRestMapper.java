package org.flexksx.platformapiservice.user.rest;

import org.flexksx.platformapiclient.user.UserResponse;
import org.flexksx.platformapiservice.user.service.User;
import org.springframework.stereotype.Component;

@Component
public class UserRestMapper {

  public UserResponse toResponse(User user) {
    return new UserResponse(user.id(), user.email());
  }
}
