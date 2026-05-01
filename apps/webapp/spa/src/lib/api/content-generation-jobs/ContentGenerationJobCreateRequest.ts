import type { ContentGenerationJobUserInput } from '../model/ContentGenerationJobUserInput';
import { ContentFormat } from '$lib/api/content/ContentFormat';

export interface ContentGenerationJobCreateRequest {
	brand_id: string;
	user_input: ContentGenerationJobUserInput;
	content_format: ContentFormat;
}
