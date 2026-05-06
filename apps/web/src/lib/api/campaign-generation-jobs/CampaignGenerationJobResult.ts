import type { ContentPillarBusinessGoal, ContentType } from '../brand-data/schema/ContentPillar';
import type { ContentDataResponse } from '../content/ContentData';
import type { ContentChannelName } from '../content-channel/ContentChannelName';
import { ContentFormat } from '../content/ContentFormat';
import { JobStatus } from '../job/JobStatus';

export interface ContentBriefCampaignGenerationJobResultResponse {
	name: string;
	description: string;
	goal: ContentPillarBusinessGoal;
	target_audience_ids: string[];
	content_pillar_ids: string[];
	start_date: string;
	end_date: string;
	channels: ContentChannelName[];
}

export interface CampaignContentPlanItemResponse {
	id: string;
	description: string;
	channel: ContentChannelName;
	content_type: ContentType;
	content_format: ContentFormat;
	image_urls: string[];
	scheduled_at: string;
	content_data: ContentDataResponse | null;
	status: JobStatus;
}

export interface CampaignGenerationJobResultResponse {
	content_brief: ContentBriefCampaignGenerationJobResultResponse | null;
	content_plan_items: CampaignContentPlanItemResponse[];
}

export class ContentBriefCampaignGenerationJobResult {
	constructor(
		public readonly name: string,
		public readonly description: string,
		public readonly goal: ContentPillarBusinessGoal,
		public readonly targetAudienceIds: string[],
		public readonly contentPillarIds: string[],
		public readonly startDate: string,
		public readonly endDate: string,
		public readonly channels: ContentChannelName[]
	) {}

	static fromResponse(
		r: ContentBriefCampaignGenerationJobResultResponse
	): ContentBriefCampaignGenerationJobResult {
		return new ContentBriefCampaignGenerationJobResult(
			r.name,
			r.description,
			r.goal,
			r.target_audience_ids,
			r.content_pillar_ids,
			r.start_date,
			r.end_date,
			r.channels
		);
	}
}

export class CampaignContentPlanItem {
	constructor(
		public readonly id: string,
		public readonly description: string,
		public readonly channel: ContentChannelName,
		public readonly contentType: ContentType,
		public readonly contentFormat: ContentFormat,
		public readonly imageUrls: string[],
		public readonly scheduledAt: string,
		public readonly contentData: ContentDataResponse | null,
		public readonly generationStatus: JobStatus
	) {}

	static fromResponse(r: CampaignContentPlanItemResponse): CampaignContentPlanItem {
		return new CampaignContentPlanItem(
			r.id,
			r.description,
			r.channel,
			r.content_type,
			r.content_format,
			r.image_urls,
			r.scheduled_at,
			r.content_data,
			r.status
		);
	}
}

export class CampaignGenerationJobResult {
	constructor(
		public readonly content_brief: ContentBriefCampaignGenerationJobResult | null,
		public readonly content_plan_items: CampaignContentPlanItem[]
	) {}

	static fromResponse(response: CampaignGenerationJobResultResponse): CampaignGenerationJobResult {
		return new CampaignGenerationJobResult(
			response.content_brief
				? ContentBriefCampaignGenerationJobResult.fromResponse(response.content_brief)
				: null,
			response.content_plan_items.map(CampaignContentPlanItem.fromResponse)
		);
	}
}
