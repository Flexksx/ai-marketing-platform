package org.flexksx.platformapiservice.user.persistence;

import org.flexksx.platformapiservice.user.service.User;
import org.springframework.stereotype.Component;

@Component
public class UserRowMapper {

  public User toDomain(UserEntity entity) {
    return new User(entity.getId(), entity.getEmail());
  }
}
