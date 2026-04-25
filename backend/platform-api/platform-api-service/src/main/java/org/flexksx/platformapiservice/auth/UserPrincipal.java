package org.flexksx.platformapiservice.auth;

import java.util.Collection;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

@RequiredArgsConstructor
public class UserPrincipal implements UserDetails {

  private final UserEntity user;

  public String getId() {
    return user.getId();
  }

  @Override
  public Collection<? extends GrantedAuthority> getAuthorities() {
    return List.of();
  }

  @Override
  public String getPassword() {
    return user.getPasswordHash();
  }

  @Override
  public String getUsername() {
    return user.getEmail();
  }
}
