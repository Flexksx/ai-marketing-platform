package org.flexksx.platformapiclient.brand.settings.contentpillar;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;
import org.flexksx.platformapiclient.brand.settings.FunnelStage;

@Schema(description = "Request object for defining a content pillar")
public record ContentPillarRequest(
    @Schema(description = "Content pillar name") @JsonProperty("name") String name,
    @Schema(description = "Topic or description of the content needed for this pillar")
        @JsonProperty("topic")
        String topic,
    @Schema(description = "Funnel stage this pillar targets") @JsonProperty("funnel_stage")
        FunnelStage funnelStage,
    @Schema(description = "Indicators of content types useful for replenishing this pillar")
        @JsonProperty("content_type_indicators")
        List<String> contentTypeIndicators) {}
