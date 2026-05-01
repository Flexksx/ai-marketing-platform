import type { CampaignState } from './CampaignState';

export interface CampaignListRequest {
	state?: CampaignState | null;
	limit?: number | null;
	offset?: number | null;
}
