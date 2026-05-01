import type { BrandListRequest } from '../brands/schema/BrandListRequest';
import type { CampaignListRequest } from '../campaign/CampaignListRequest';
import type { ContentListRequest } from '../content/ContentListRequest';

export const queryKeys = {
	brand: (id: string) => ['brand', id] as const,
	brands: (params?: BrandListRequest) => ['brands', params] as const,
	content: (id: string) => ['content', id] as const,
	contentForBrand: (brandId: string, params?: ContentListRequest) =>
		['content', 'brand', brandId, params] as const,
	campaignsForBrand: (brandId: string, params?: CampaignListRequest) =>
		['campaigns', 'brand', brandId, params] as const,
	brandGenerationJob: (jobId: string) => ['brandGenerationJob', jobId] as const,
	campaignGenerationJob: (jobId: string) => ['campaignGenerationJob', jobId] as const,
	contentGenerationJob: (jobId: string) => ['contentGenerationJob', jobId] as const,
	contentGenerationJobs: (brandId: string) => ['contentGenerationJobs', brandId] as const
};
