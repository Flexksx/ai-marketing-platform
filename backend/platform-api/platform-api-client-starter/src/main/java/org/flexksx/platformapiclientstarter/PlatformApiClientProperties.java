package org.flexksx.platformapiclientstarter;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "platform.api")
public record PlatformApiClientProperties(String baseUrl) {}
