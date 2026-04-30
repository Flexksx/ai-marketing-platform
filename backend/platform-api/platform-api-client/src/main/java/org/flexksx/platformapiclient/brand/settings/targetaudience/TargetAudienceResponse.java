package org.flexksx.platformapiclient.brand.settings.targetaudience;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;
import org.flexksx.platformapiclient.brand.settings.FunnelStage;

@Schema(description = "A target audience segment mapped to a funnel stage")
public record TargetAudienceResponse(
    @Schema(description = "Audience unique identifier") @JsonProperty("id") String id,
    @Schema(description = "Audience name") @JsonProperty("name") String name,
    @Schema(description = "Funnel stage this audience belongs to") @JsonProperty("funnel_stage")
        FunnelStage funnelStage,
    @Schema(description = "What this audience desires") @JsonProperty("desires")
        List<String> desires,
    @Schema(description = "Pain points this audience experiences") @JsonProperty("pain_points")
        List<String> painPoints,
    @Schema(description = "ID of the content pillar mapped to this audience")
        @JsonProperty("content_pillar_id")
        String contentPillarId) {}
