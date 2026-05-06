import type { JobStatus } from '../job/JobStatus';
import {
	ContentGenerationJobUserInput,
	type ContentGenerationJobUserInputResponse
} from './ContentGenerationJobUserInput';
import type { ContentFormat } from '../content/ContentFormat';
import {
	ContentGenerationJobResult,
	type ContentGenerationJobResultResponse
} from './ContentGenerationJobResult';

export interface ContentGenerationJobResponse {
	id: string;
	brand_id: string;
	status: JobStatus;
	content_format: ContentFormat;
	user_input: ContentGenerationJobUserInputResponse;
	result: ContentGenerationJobResultResponse | null;
	created_at: string;
	updated_at: string;
}

export class ContentGenerationJob {
	constructor(
		public readonly id: string,
		public readonly brandId: string,
		public readonly status: JobStatus,
		public readonly contentFormat: ContentFormat,
		public readonly userInput: ContentGenerationJobUserInput,
		public readonly result: ContentGenerationJobResult | null,
		public readonly createdAt: string,
		public readonly updatedAt: string
	) {}
	static fromResponse(response: ContentGenerationJobResponse): ContentGenerationJob {
		return new ContentGenerationJob(
			response.id,
			response.brand_id,
			response.status,
			response.content_format,
			ContentGenerationJobUserInput.fromResponse(response.user_input),
			response.result ? ContentGenerationJobResult.fromResponse(response.result) : null,
			response.created_at,
			response.updated_at
		);
	}
}
