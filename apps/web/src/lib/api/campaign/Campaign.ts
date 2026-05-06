import { CampaignData, type CampaignDataResponse } from './CampaignData';
import type { CampaignState } from './CampaignState';

export interface CampaignResponse {
	id: string;
	brand_id: string;
	state: CampaignState;
	data: CampaignDataResponse;
	created_at: string;
	updated_at: string;
}

export class Campaign {
	constructor(
		public readonly id: string,
		public readonly brandId: string,
		public readonly state: CampaignState,
		public readonly data: CampaignData | null,
		public readonly createdAt: string,
		public readonly updatedAt: string
	) {}

	static fromResponse(response: CampaignResponse): Campaign {
		return new Campaign(
			response.id,
			response.brand_id,
			response.state,
			CampaignData.fromResponse(response.data),
			response.created_at,
			response.updated_at
		);
	}
}
