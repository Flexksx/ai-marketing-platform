package org.flexksx.platformapiservice.brand.persistence;

import java.util.List;

public record ContentPillarJson(
    String id, String name, String topic, String funnelStage, List<String> contentTypeIndicators) {}
