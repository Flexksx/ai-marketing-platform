package org.flexksx.platformapiservice.user.service;

import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.auth.InvalidCredentialsException;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.flexksx.platformapiservice.user.persistence.UserRepository;
import org.flexksx.platformapiservice.user.persistence.UserRowMapper;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

  private final UserRepository userRepository;
  private final UserRowMapper userRowMapper;
  private final PasswordEncoder passwordEncoder;

  public User get(String id) {
    return userRepository
        .findById(id)
        .map(userRowMapper::toDomain)
        .orElseThrow(() -> new UserNotFoundException(id));
  }

  @Transactional
  public User updateEmail(String id, String newEmail) {
    UserEntity user = userRepository.findById(id).orElseThrow(() -> new UserNotFoundException(id));
    user.setEmail(newEmail);
    return userRowMapper.toDomain(userRepository.save(user));
  }

  @Transactional
  public void changePassword(String id, String oldPassword, String newPassword) {
    UserEntity user = userRepository.findById(id).orElseThrow(() -> new UserNotFoundException(id));
    if (!passwordEncoder.matches(oldPassword, user.getPasswordHash())) {
      throw new InvalidCredentialsException();
    }
    user.setPasswordHash(passwordEncoder.encode(newPassword));
    // Invalidate all existing tokens after password change
    user.incrementTokenVersion();
    userRepository.save(user);
  }
}
