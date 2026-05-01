import type { BrandDataResponse } from '$lib/api/brand-data/schema/BrandData';

export interface BrandResponse {
	id: string;
	name: string;
	data: BrandDataResponse | null;
	created_at: string;
	updated_at: string;
}
