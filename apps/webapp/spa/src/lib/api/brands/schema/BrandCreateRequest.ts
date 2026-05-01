import type { BrandDataResponse } from '$lib/api/brand-data/schema/BrandData';

export interface BrandCreateRequest {
	name: string;
	data: BrandDataResponse;
}
