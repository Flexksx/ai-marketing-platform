package org.flexksx.platformapiservice.brand.service;

import java.time.Instant;
import java.util.List;

public record BrandData(
    String logoUrl,
    String websiteUrl,
    String description,
    Instant createdAt,
    Instant updatedAt,
    List<TargetAudience> targetAudiences,
    List<ContentPillar> contentPillars) {}
