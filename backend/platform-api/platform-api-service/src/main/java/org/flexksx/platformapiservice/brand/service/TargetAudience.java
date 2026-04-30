package org.flexksx.platformapiservice.brand.service;

import java.util.List;

public record TargetAudience(
    String id,
    String name,
    FunnelStage funnelStage,
    List<String> desires,
    List<String> painPoints,
    String contentPillarId) {}
