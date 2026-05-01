import { brandDataFromResponse } from '$lib/api/brand-data/model/BrandData';
import type { BrandDataParsed } from './BrandData';
import type { BrandResponse } from '$lib/api/brands/schema/BrandResponse';

export class Brand {
	constructor(
		public readonly id: string,
		public readonly name: string,
		public readonly data: BrandDataParsed | null,
		public readonly created_at: string,
		public readonly updated_at: string
	) {}

	static fromResponse(response: BrandResponse): Brand {
		return new Brand(
			response.id,
			response.name,
			response.data ? brandDataFromResponse(response.data) : null,
			response.created_at,
			response.updated_at
		);
	}
}
