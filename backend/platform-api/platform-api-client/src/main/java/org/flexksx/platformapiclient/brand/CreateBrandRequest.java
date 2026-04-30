package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;
import org.flexksx.platformapiclient.brand.settings.contentpillar.ContentPillarRequest;
import org.flexksx.platformapiclient.brand.settings.targetaudience.TargetAudienceRequest;

@Schema(description = "Request object for creating a new brand")
public record CreateBrandRequest(
    @Schema(description = "Name of the brand") @JsonProperty("name") String name,
    @Schema(description = "URL to the brand's website") @JsonProperty("website_url")
        String websiteUrl,
    @Schema(description = "Brand description") @JsonProperty("description") String description,
    @Schema(description = "Target audiences segmented by funnel stage")
        @JsonProperty("target_audiences")
        List<TargetAudienceRequest> targetAudiences,
    @Schema(description = "Content pillars mapped to each funnel stage")
        @JsonProperty("content_pillars")
        List<ContentPillarRequest> contentPillars) {}
