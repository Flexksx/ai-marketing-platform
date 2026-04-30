package org.flexksx.platformapiservice.brand.persistence;

import java.util.Collections;
import java.util.List;
import org.flexksx.platformapiservice.brand.service.Brand;
import org.flexksx.platformapiservice.brand.service.BrandData;
import org.flexksx.platformapiservice.brand.service.ContentPillar;
import org.flexksx.platformapiservice.brand.service.FunnelStage;
import org.flexksx.platformapiservice.brand.service.TargetAudience;
import org.springframework.stereotype.Component;

@Component
public class BrandRowMapper {

  public Brand toDomain(BrandEntity entity) {
    BrandData data =
        new BrandData(
            entity.getLogoUrl(),
            entity.getWebsiteUrl(),
            entity.getDescription(),
            entity.getCreatedAt(),
            entity.getUpdatedAt(),
            toTargetAudienceDomain(entity.getTargetAudiences()),
            toContentPillarDomain(entity.getContentPillars()));
    return new Brand(entity.getId(), entity.getName(), data);
  }

  public BrandEntity toEntity(Brand brand) {
    BrandData data = brand.data();
    if (data == null) {
      return new BrandEntity(brand.id(), brand.name(), null, null, null, null, null, null, null);
    }
    return new BrandEntity(
        brand.id(),
        brand.name(),
        data.logoUrl(),
        data.websiteUrl(),
        data.description(),
        data.createdAt(),
        data.updatedAt(),
        toTargetAudienceJson(data.targetAudiences()),
        toContentPillarJson(data.contentPillars()));
  }

  private List<TargetAudience> toTargetAudienceDomain(List<TargetAudienceJson> jsonList) {
    if (jsonList == null) {
      return Collections.emptyList();
    }
    return jsonList.stream()
        .map(
            json ->
                new TargetAudience(
                    json.id(),
                    json.name(),
                    FunnelStage.valueOf(json.funnelStage()),
                    json.desires(),
                    json.painPoints(),
                    json.contentPillarId()))
        .toList();
  }

  private List<ContentPillar> toContentPillarDomain(List<ContentPillarJson> jsonList) {
    if (jsonList == null) {
      return Collections.emptyList();
    }
    return jsonList.stream()
        .map(
            json ->
                new ContentPillar(
                    json.id(),
                    json.name(),
                    json.topic(),
                    FunnelStage.valueOf(json.funnelStage()),
                    json.contentTypeIndicators()))
        .toList();
  }

  private List<TargetAudienceJson> toTargetAudienceJson(List<TargetAudience> audiences) {
    if (audiences == null) {
      return Collections.emptyList();
    }
    return audiences.stream()
        .map(
            audience ->
                new TargetAudienceJson(
                    audience.id(),
                    audience.name(),
                    audience.funnelStage().name(),
                    audience.desires(),
                    audience.painPoints(),
                    audience.contentPillarId()))
        .toList();
  }

  private List<ContentPillarJson> toContentPillarJson(List<ContentPillar> pillars) {
    if (pillars == null) {
      return Collections.emptyList();
    }
    return pillars.stream()
        .map(
            pillar ->
                new ContentPillarJson(
                    pillar.id(),
                    pillar.name(),
                    pillar.topic(),
                    pillar.funnelStage().name(),
                    pillar.contentTypeIndicators()))
        .toList();
  }
}
