import type { ContentChannelName } from '../content-channel/ContentChannelName';
import type { CampaignGenerationJobWorkflowType } from './CampaignGenerationJobWorkflowType';

export interface CampaignGenerationJobCreateRequest {
	brand_id: string;
	prompt: string;
	start_date: string;
	end_date: string;
	channels: ContentChannelName[];
	workflow_type: CampaignGenerationJobWorkflowType;
}
