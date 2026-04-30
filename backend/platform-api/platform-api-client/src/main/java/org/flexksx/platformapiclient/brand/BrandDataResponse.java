package org.flexksx.platformapiclient.brand;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;
import java.util.List;
import org.flexksx.platformapiclient.brand.settings.contentpillar.ContentPillarResponse;
import org.flexksx.platformapiclient.brand.settings.targetaudience.TargetAudienceResponse;

@Schema(description = "Response object containing brand metadata")
public record BrandDataResponse(
    @Schema(description = "URL to the brand's logo") @JsonProperty("logo_url") String logoUrl,
    @Schema(description = "URL to the brand's website") @JsonProperty("website_url")
        String websiteUrl,
    @Schema(description = "Brand description") @JsonProperty("description") String description,
    @Schema(description = "Timestamp when the brand was created") @JsonProperty("created_at")
        Instant createdAt,
    @Schema(description = "Timestamp when the brand was last updated") @JsonProperty("updated_at")
        Instant updatedAt,
    @Schema(description = "Target audiences segmented by funnel stage")
        @JsonProperty("target_audiences")
        List<TargetAudienceResponse> targetAudiences,
    @Schema(description = "Content pillars mapped to each funnel stage")
        @JsonProperty("content_pillars")
        List<ContentPillarResponse> contentPillars) {}
