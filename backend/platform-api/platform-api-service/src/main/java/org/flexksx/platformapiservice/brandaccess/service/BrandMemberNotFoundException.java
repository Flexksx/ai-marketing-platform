package org.flexksx.platformapiservice.brandaccess.service;

public class BrandMemberNotFoundException extends RuntimeException {

  public BrandMemberNotFoundException(String userId, String brandId) {
    super(String.format("User %s is not a member of brand %s", userId, brandId));
  }
}
