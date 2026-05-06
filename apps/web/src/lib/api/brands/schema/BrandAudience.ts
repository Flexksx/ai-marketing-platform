import type { BrandAudience } from '$lib/api/brand-data/model/BrandData';
import type { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';
import type { BrandAudienceAgeRange } from './BrandAudienceAgeRange';
import type { BrandAudienceGender } from './BrandAudienceGender';
import type { BrandAudienceIncomeRange } from './BrandAudienceIncomeRange';

export interface BrandAudienceResponse {
	id: string;
	name: string;
	location?: string | null;
	age_range: BrandAudienceAgeRange;
	gender: BrandAudienceGender;
	income_range: BrandAudienceIncomeRange;
	pain_points: string[];
	desired_outcomes: string[];
	objections: string[];
	channels: ContentChannelName[];
}

export function audienceFromResponse(response: BrandAudienceResponse): BrandAudience {
	return {
		id: response.id,
		name: response.name,
		ageRange: response.age_range,
		gender: response.gender,
		incomeRange: response.income_range,
		painPoints: response.pain_points,
		objections: response.objections,
		channels: response.channels
	};
}

export function audienceToRequest(audience: BrandAudience): BrandAudienceResponse {
	return {
		id: audience.id,
		name: audience.name,
		location: null,
		age_range: audience.ageRange,
		gender: audience.gender,
		income_range: audience.incomeRange,
		pain_points: audience.painPoints,
		desired_outcomes: [],
		objections: audience.objections,
		channels: audience.channels
	};
}
