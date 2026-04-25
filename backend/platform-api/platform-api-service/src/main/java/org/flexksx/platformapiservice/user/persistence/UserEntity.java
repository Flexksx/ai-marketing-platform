package org.flexksx.platformapiservice.user.persistence;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class UserEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  private String id;

  @Setter
  @Column(name = "email", nullable = false, unique = true)
  private String email;

  @Setter
  @Column(name = "password_hash", nullable = false)
  private String passwordHash;

  @Column(name = "token_version", nullable = false)
  private Integer tokenVersion;

  public static UserEntity create(String email, String passwordHash) {
    return new UserEntity(null, email, passwordHash, 0);
  }

  public void incrementTokenVersion() {
    this.tokenVersion++;
  }
}
