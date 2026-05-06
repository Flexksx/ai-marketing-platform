import { BrandArchetypeName } from '$lib/api/brands/schema/BrandArchetypeName';
import { BrandAudienceAgeRange } from '$lib/api/brands/schema/BrandAudienceAgeRange';
import { BrandAudienceGender } from '$lib/api/brands/schema/BrandAudienceGender';
import { BrandAudienceIncomeRange } from '$lib/api/brands/schema/BrandAudienceIncomeRange';
import type { BrandColor } from '$lib/api/brands/schema/BrandColor';
import { SentenceLengthPreference } from '$lib/api/brands/schema/BrandToneOfVoice';
import type { BrandToneOfVoice } from '$lib/api/brands/schema/BrandToneOfVoice';
import {
	contentPillarFromResponse,
	ContentPillarBusinessGoal,
	ContentPillarFunnelStage,
	ContentPillarType
} from '$lib/api/brand-data/schema/ContentPillar';
import type { ContentPillarParsed } from '$lib/api/brand-data/schema/ContentPillar';
import { audienceFromResponse } from '$lib/api/brands/schema/BrandAudience';
import { positioningFromResponse } from '$lib/api/brand-data/schema/PositioningBrandData';
import type { BrandDataResponse } from '$lib/api/brand-data/schema/BrandData';
import type { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';

export { BrandArchetypeName } from '$lib/api/brands/schema/BrandArchetypeName';
export { BrandAudienceAgeRange } from '$lib/api/brands/schema/BrandAudienceAgeRange';
export { BrandAudienceGender } from '$lib/api/brands/schema/BrandAudienceGender';
export { BrandAudienceIncomeRange } from '$lib/api/brands/schema/BrandAudienceIncomeRange';
export type { BrandColor } from '$lib/api/brands/schema/BrandColor';
export { SentenceLengthPreference } from '$lib/api/brands/schema/BrandToneOfVoice';
export type { BrandToneOfVoice } from '$lib/api/brands/schema/BrandToneOfVoice';
export type { ContentPillarParsed } from '$lib/api/brand-data/schema/ContentPillar';
export {
	ContentPillarBusinessGoal,
	ContentPillarFunnelStage,
	ContentPillarType,
	ContentType
} from '$lib/api/brand-data/schema/ContentPillar';

export interface BrandAudience {
	id: string;
	name: string;
	ageRange: BrandAudienceAgeRange;
	gender: BrandAudienceGender;
	incomeRange: BrandAudienceIncomeRange;
	painPoints: string[];
	objections: string[];
	channels: ContentChannelName[];
}

export interface PositioningBrandDataParsed {
	description: string;
	pointsOfParity: string[];
	pointsOfDifference: string[];
	productDescription: string;
}

export interface BrandDataParsed {
	logoUrl: string | null;
	mediaUrls: string[];
	colors: BrandColor[];
	brandMission: string | null;
	archetype: BrandArchetypeName | null;
	locale: string | null;
	audiences: BrandAudience[];
	contentPillars: ContentPillarParsed[];
	toneOfVoice: BrandToneOfVoice;
	positioning: PositioningBrandDataParsed;
}

export interface BrandSettingsFormData {
	name: string;
	logoUrl: string;
	description: string;
	brandMission: string;
	archetype: string;
	locale: string | null;
	colors: BrandColor[];
	mediaUrls: string[];
	audiences: BrandAudience[];
	contentPillars: ContentPillarParsed[];
	toneOfVoice: BrandToneOfVoice | null;
	positioningPointsOfParity: string[];
	positioningPointsOfDifference: string[];
	productDescription: string;
	pendingLogoFile: File | null;
}

export const defaultToneOfVoice: BrandToneOfVoice = {
	formality_level: 1,
	humour_level: 1,
	irreverence_level: 1,
	enthusiasm_level: 1,
	industry_jargon_usage_level: 1,
	sentence_length_preference: SentenceLengthPreference.MEDIUM,
	sensory_keywords: [],
	excluded_words: [],
	signature_words: []
};

export function createEmptyBrandSettingsFormData(): BrandSettingsFormData {
	return {
		name: '',
		logoUrl: '',
		description: '',
		brandMission: '',
		archetype: '',
		locale: null,
		colors: [],
		mediaUrls: [],
		audiences: [],
		contentPillars: [],
		toneOfVoice: null,
		positioningPointsOfParity: [],
		positioningPointsOfDifference: [],
		productDescription: '',
		pendingLogoFile: null
	};
}

export function brandDataFromResponse(response: BrandDataResponse): BrandDataParsed {
	return {
		logoUrl: response.logo_url ?? null,
		mediaUrls: response.media_urls ?? [],
		colors: response.colors ?? [],
		brandMission: response.brand_mission ?? null,
		archetype: response.archetype ?? null,
		locale: response.locale ?? null,
		audiences: (response.audiences ?? []).map(audienceFromResponse),
		contentPillars: (response.content_pillars ?? []).map(contentPillarFromResponse),
		toneOfVoice: response.tone_of_voice,
		positioning: positioningFromResponse(response.positioning)
	};
}

export function createDefaultContentPillar(): ContentPillarParsed {
	return {
		id: crypto.randomUUID(),
		name: '',
		businessGoal: ContentPillarBusinessGoal.DRIVE_ENGAGEMENT,
		type: ContentPillarType.EDUCATION,
		funnelStage: ContentPillarFunnelStage.AWARENESS,
		contentTypes: [],
		audienceIds: [],
		hooks: [],
		callsToAction: []
	};
}
