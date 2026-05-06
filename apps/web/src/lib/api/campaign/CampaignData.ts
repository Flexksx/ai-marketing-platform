import type { ContentPillarBusinessGoal } from '$lib/api/brand-data/schema/ContentPillar';
import type { ContentChannelName } from '../content-channel/ContentChannelName';

export interface CampaignDataResponse {
	name: string;
	goal: ContentPillarBusinessGoal;
	description: string;
	target_audience_ids: string[];
	content_pillar_ids: string[];
	content_ids: string[];
	channels: ContentChannelName[];
	media_urls: string[];
	start_date: string;
	end_date: string;
}

export class CampaignData {
	constructor(
		public readonly name: string,
		public readonly goal: ContentPillarBusinessGoal,
		public readonly description: string,
		public readonly targetAudienceIds: string[],
		public readonly contentPillarIds: string[],
		public readonly contentIds: string[],
		public readonly channels: ContentChannelName[],
		public readonly mediaUrls: string[],
		public readonly startDate: string,
		public readonly endDate: string
	) {}
	static fromResponse(response: CampaignDataResponse): CampaignData {
		return new CampaignData(
			response.name,
			response.goal,
			response.description,
			response.target_audience_ids ?? [],
			response.content_pillar_ids ?? [],
			response.content_ids ?? [],
			response.channels ?? [],
			response.media_urls ?? [],
			response.start_date,
			response.end_date
		);
	}
}
