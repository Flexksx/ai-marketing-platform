package org.flexksx.platformapiservice.brandaccess.service;

public class BrandMemberAlreadyExistsException extends RuntimeException {

  public BrandMemberAlreadyExistsException(String userId, String brandId) {
    super(String.format("User %s is already a member of brand %s", userId, brandId));
  }
}
