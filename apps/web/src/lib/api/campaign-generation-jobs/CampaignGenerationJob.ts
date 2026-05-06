import type { JobStatus } from '../job/JobStatus';
import {
	CampaignGenerationJobUserInput,
	type CampaignGenerationJobUserInputResponse
} from './CampaignGenerationJobUserInput';
import {
	CampaignGenerationJobResult,
	type CampaignGenerationJobResultResponse
} from './CampaignGenerationJobResult';

export interface CampaignGenerationJobResponse {
	id: string;
	brand_id: string;
	user_input: CampaignGenerationJobUserInputResponse;
	status: JobStatus;
	result: CampaignGenerationJobResultResponse | null;
	created_at: string;
	updated_at: string;
}

export class CampaignGenerationJob {
	constructor(
		public readonly id: string,
		public readonly brandId: string,
		public readonly userInput: CampaignGenerationJobUserInput,
		public readonly status: JobStatus,
		public readonly result: CampaignGenerationJobResult | null,
		public readonly createdAt: string,
		public readonly updatedAt: string
	) {}

	public static fromResponse(response: CampaignGenerationJobResponse): CampaignGenerationJob {
		return new CampaignGenerationJob(
			response.id,
			response.brand_id,
			CampaignGenerationJobUserInput.fromResponse(response.user_input),
			response.status,
			response.result ? CampaignGenerationJobResult.fromResponse(response.result) : null,
			response.created_at,
			response.updated_at
		);
	}
}
