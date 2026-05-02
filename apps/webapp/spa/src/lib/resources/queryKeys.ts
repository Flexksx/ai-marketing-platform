import type { BrandCampaignsListRequest } from '$lib/api/generated/apis/BrandCampaignsApi';
import type { BrandsSearchRequest } from '$lib/api/generated/apis/BrandsApi';
import type { BrandContentSearchRequest } from '$lib/api/generated/apis/BrandContentApi';

export const queryKeys = {
	brand: (id: string) => ['brand', id] as const,
	brands: (params?: BrandsSearchRequest) => ['brands', params] as const,
	content: (id: string) => ['content', id] as const,
	contentForBrand: (brandId: string, params?: BrandContentSearchRequest) =>
		['content', 'brand', brandId, params] as const,
	campaignsForBrand: (brandId: string, params?: BrandCampaignsListRequest) =>
		['campaigns', 'brand', brandId, params] as const,
	brandGenerationJob: (jobId: string) => ['brandGenerationJob', jobId] as const,
	campaignGenerationJob: (jobId: string) => ['campaignGenerationJob', jobId] as const,
	contentGenerationJob: (jobId: string) => ['contentGenerationJob', jobId] as const,
	contentGenerationJobs: (brandId: string) => ['contentGenerationJobs', brandId] as const
};
