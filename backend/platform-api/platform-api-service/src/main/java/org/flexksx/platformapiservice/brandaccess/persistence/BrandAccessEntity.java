package org.flexksx.platformapiservice.brandaccess.persistence;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.flexksx.platformapiservice.brandaccess.service.BrandMemberRole;

@Entity
@Table(
    name = "user_brand_memberships",
    uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "brand_id"}))
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class BrandAccessEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  private String id;

  @Column(name = "user_id", nullable = false)
  private String userId;

  @Column(name = "brand_id", nullable = false)
  private String brandId;

  @Enumerated(EnumType.STRING)
  @Column(name = "role", nullable = false)
  private BrandMemberRole role;

  public static BrandAccessEntity of(String userId, String brandId, BrandMemberRole role) {
    return new BrandAccessEntity(null, userId, brandId, role);
  }

  public void setRole(BrandMemberRole role) {
    this.role = role;
  }
}
