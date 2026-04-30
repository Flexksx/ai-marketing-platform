package org.flexksx.platformapiservice.brand.persistence;

import java.util.List;

public record TargetAudienceJson(
    String id,
    String name,
    String funnelStage,
    List<String> desires,
    List<String> painPoints,
    String contentPillarId) {}
