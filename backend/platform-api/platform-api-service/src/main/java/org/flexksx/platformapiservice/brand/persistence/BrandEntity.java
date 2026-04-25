package org.flexksx.platformapiservice.brand.persistence;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "brands")
public class BrandEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  private String id;

  @Column(name = "name", nullable = false)
  private String name;

  @Column(name = "logo_url")
  private String logoUrl;

  @Column(name = "website_url")
  private String websiteUrl;

  public BrandEntity() {}

  public BrandEntity(String id, String name, String logoUrl, String websiteUrl) {
    this.id = id;
    this.name = name;
    this.logoUrl = logoUrl;
    this.websiteUrl = websiteUrl;
  }

  public String getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public String getLogoUrl() {
    return logoUrl;
  }

  public String getWebsiteUrl() {
    return websiteUrl;
  }
}
