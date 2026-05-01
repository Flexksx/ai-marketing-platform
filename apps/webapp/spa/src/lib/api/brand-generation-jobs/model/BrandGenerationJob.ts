import { brandDataFromResponse } from '$lib/api/brand-data/model/BrandData';
import type { BrandDataParsed } from '$lib/api/brand-data/model/BrandData';
import type { BrandGenerationJobResponse } from '../schema/BrandGenerationJobResponse';

export type BrandGenerationJobStatus =
	| 'pending'
	| 'in_progress'
	| 'completed'
	| 'failed'
	| 'cancelled';

export interface ScrapeResult {
	text: string;
	imageUrls: string[];
	videoUrls: string[];
	logo: string | null;
	screenshot: string | null;
	pageUrls: string[];
}

export interface BrandGenerationJobResult {
	brandData: { name: string; data: BrandDataParsed } | null;
	scraperResult: ScrapeResult | null;
}

export class BrandGenerationJob {
	constructor(
		public readonly id: string,
		public readonly status: BrandGenerationJobStatus,
		public readonly result: BrandGenerationJobResult | null,
		public readonly createdAt: string,
		public readonly updatedAt: string
	) {}

	static fromResponse(response: BrandGenerationJobResponse): BrandGenerationJob {
		const result = response.result
			? {
					brandData: response.result.brand_data
						? {
								name: response.result.brand_data.name,
								data: brandDataFromResponse(response.result.brand_data.data)
							}
						: null,
					scraperResult: response.result.scraper_result
						? {
								text: response.result.scraper_result.text,
								imageUrls: response.result.scraper_result.image_urls,
								videoUrls: response.result.scraper_result.video_urls,
								logo: response.result.scraper_result.logo,
								screenshot: response.result.scraper_result.screenshot,
								pageUrls: response.result.scraper_result.page_urls
							}
						: null
				}
			: null;

		return new BrandGenerationJob(
			response.id,
			response.status,
			result,
			response.created_at,
			response.updated_at
		);
	}
}
