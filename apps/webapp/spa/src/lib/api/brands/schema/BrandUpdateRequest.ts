import type { BrandDataUpdateRequest } from './BrandDataUpdateRequest';

export interface BrandUpdateRequest {
	name?: string | null;
	data?: BrandDataUpdateRequest | null;
}
