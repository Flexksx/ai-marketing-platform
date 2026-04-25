package org.flexksx.platformapiservice.brandcontentitems.persistence;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "content_items")
public class ContentItemEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  private String id;

  @Column(name = "brand_id", nullable = false)
  private String brandId;

  public ContentItemEntity() {}

  public ContentItemEntity(String id, String brandId) {
    this.id = id;
    this.brandId = brandId;
  }

  public String getId() {
    return id;
  }

  public String getBrandId() {
    return brandId;
  }
}
