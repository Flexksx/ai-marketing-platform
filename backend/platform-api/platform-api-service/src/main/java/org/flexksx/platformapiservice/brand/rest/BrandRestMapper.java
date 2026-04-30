package org.flexksx.platformapiservice.brand.rest;

import java.util.Collections;
import java.util.List;
import java.util.UUID;
import org.flexksx.platformapiclient.brand.BrandDataResponse;
import org.flexksx.platformapiclient.brand.BrandResponse;
import org.flexksx.platformapiclient.brand.CreateBrandRequest;
import org.flexksx.platformapiclient.brand.settings.FunnelStage;
import org.flexksx.platformapiclient.brand.settings.contentpillar.ContentPillarRequest;
import org.flexksx.platformapiclient.brand.settings.contentpillar.ContentPillarResponse;
import org.flexksx.platformapiclient.brand.settings.targetaudience.TargetAudienceRequest;
import org.flexksx.platformapiclient.brand.settings.targetaudience.TargetAudienceResponse;
import org.flexksx.platformapiservice.brand.service.Brand;
import org.flexksx.platformapiservice.brand.service.BrandData;
import org.flexksx.platformapiservice.brand.service.ContentPillar;
import org.flexksx.platformapiservice.brand.service.TargetAudience;
import org.springframework.stereotype.Component;

@Component
public class BrandRestMapper {

  public BrandResponse toResponse(Brand brand) {
    BrandData data = brand.data();
    BrandDataResponse dataResponse =
        new BrandDataResponse(
            data.logoUrl(),
            data.websiteUrl(),
            data.description(),
            data.createdAt(),
            data.updatedAt(),
            toTargetAudienceResponse(data.targetAudiences()),
            toContentPillarResponse(data.contentPillars()));
    return new BrandResponse(brand.id(), brand.name(), dataResponse);
  }

  public Brand toDomain(CreateBrandRequest request) {
    BrandData data =
        new BrandData(
            null,
            request.websiteUrl(),
            request.description(),
            null,
            null,
            toTargetAudienceDomain(request.targetAudiences()),
            toContentPillarDomain(request.contentPillars()));
    return new Brand(null, request.name(), data);
  }

  private List<TargetAudienceResponse> toTargetAudienceResponse(List<TargetAudience> audiences) {
    if (audiences == null) {
      return Collections.emptyList();
    }
    return audiences.stream()
        .map(
            audience ->
                new TargetAudienceResponse(
                    audience.id(),
                    audience.name(),
                    FunnelStage.valueOf(audience.funnelStage().name()),
                    audience.desires(),
                    audience.painPoints(),
                    audience.contentPillarId()))
        .toList();
  }

  private List<ContentPillarResponse> toContentPillarResponse(List<ContentPillar> pillars) {
    if (pillars == null) {
      return Collections.emptyList();
    }
    return pillars.stream()
        .map(
            pillar ->
                new ContentPillarResponse(
                    pillar.id(),
                    pillar.name(),
                    pillar.topic(),
                    FunnelStage.valueOf(pillar.funnelStage().name()),
                    pillar.contentTypeIndicators()))
        .toList();
  }

  private List<TargetAudience> toTargetAudienceDomain(List<TargetAudienceRequest> requests) {
    if (requests == null) {
      return Collections.emptyList();
    }
    return requests.stream()
        .map(
            request ->
                new TargetAudience(
                    UUID.randomUUID().toString(),
                    request.name(),
                    org.flexksx.platformapiservice.brand.service.FunnelStage.valueOf(
                        request.funnelStage().name()),
                    request.desires(),
                    request.painPoints(),
                    null))
        .toList();
  }

  private List<ContentPillar> toContentPillarDomain(List<ContentPillarRequest> requests) {
    if (requests == null) {
      return Collections.emptyList();
    }
    return requests.stream()
        .map(
            request ->
                new ContentPillar(
                    UUID.randomUUID().toString(),
                    request.name(),
                    request.topic(),
                    org.flexksx.platformapiservice.brand.service.FunnelStage.valueOf(
                        request.funnelStage().name()),
                    request.contentTypeIndicators()))
        .toList();
  }
}
