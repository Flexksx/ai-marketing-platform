package org.flexksx.platformapiservice.brand.service;

import java.util.List;

public record ContentPillar(
    String id,
    String name,
    String topic,
    FunnelStage funnelStage,
    List<String> contentTypeIndicators) {}
