package org.flexksx.platformapiservice.brand.service;

public class BrandNotFoundException extends RuntimeException {

  private static final String MESSAGE_TEMPLATE = "Brand not found with id: %s";

  public BrandNotFoundException(String id) {
    super(String.format(MESSAGE_TEMPLATE, id));
  }
}
