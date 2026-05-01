import type { PositioningBrandDataParsed } from '../model/BrandData';

export interface PositioningBrandDataResponse {
	description: string;
	points_of_difference: string[];
	points_of_parity: string[];
	product_description: string;
}

export function positioningFromResponse(
	response: PositioningBrandDataResponse
): PositioningBrandDataParsed {
	return {
		description: response.description,
		pointsOfDifference: response.points_of_difference,
		pointsOfParity: response.points_of_parity,
		productDescription: response.product_description
	};
}
