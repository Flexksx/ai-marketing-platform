package org.flexksx.platformapiservice.user.service;

public class UserNotFoundException extends RuntimeException {

  private static final String MESSAGE_TEMPLATE = "User not found with id: %s";

  public UserNotFoundException(String id) {
    super(String.format(MESSAGE_TEMPLATE, id));
  }
}
