import type { BrandDataResponse } from '$lib/api/brand-data/schema/BrandData';
import type { BrandGenerationJobStatus } from '../model/BrandGenerationJob';
import type { ScrapeResultResponse } from './ScrapeResult';

export interface BrandDataResultResponse {
	name: string;
	data: BrandDataResponse;
}

export interface BrandGenerationJobResultResponse {
	brand_data: BrandDataResultResponse | null;
	scraper_result: ScrapeResultResponse | null;
}

export interface BrandGenerationJobResponse {
	id: string;
	status: BrandGenerationJobStatus;
	result: BrandGenerationJobResultResponse | null;
	created_at: string;
	updated_at: string;
}
