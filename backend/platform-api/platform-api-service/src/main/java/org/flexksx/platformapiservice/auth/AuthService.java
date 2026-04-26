package org.flexksx.platformapiservice.auth;

import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.flexksx.platformapiservice.user.persistence.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuthService {

  private final UserRepository userRepository;
  private final JwtService jwtService;
  private final PasswordEncoder passwordEncoder;

  public String login(String email, String password) {
    UserEntity user =
        userRepository.findByEmail(email).orElseThrow(() -> new InvalidCredentialsException());
    if (!passwordEncoder.matches(password, user.getPasswordHash())) {
      throw new InvalidCredentialsException();
    }
    return jwtService.issue(user);
  }

  @Transactional
  public String register(String email, String password) {
    if (userRepository.findByEmail(email).isPresent()) {
      throw new EmailAlreadyRegisteredException(email);
    }
    UserEntity user =
        userRepository.save(
            UserEntity.create(email, passwordEncoder.encode(password)));
    return jwtService.issue(user);
  }

  @Transactional
  public void logout(String userId) {
    UserEntity user = userRepository.findById(userId).orElseThrow();
    user.incrementTokenVersion();
    userRepository.save(user);
  }
}
