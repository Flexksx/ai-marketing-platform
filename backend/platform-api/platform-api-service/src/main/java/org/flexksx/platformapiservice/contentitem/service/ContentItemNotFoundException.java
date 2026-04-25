package org.flexksx.platformapiservice.contentitem.service;

public class ContentItemNotFoundException extends RuntimeException {

  private static final String MESSAGE_TEMPLATE = "Content item not found with id: %s for brand: %s";

  public ContentItemNotFoundException(String id, String brandId) {
    super(String.format(MESSAGE_TEMPLATE, id, brandId));
  }
}
