import type { BrandSettingsFormData } from '$lib/api/brand-data/model/BrandData';
import { audienceToRequest } from '$lib/api/brands/schema/BrandAudience';
import type { BrandArchetypeName } from '$lib/api/brands/schema/BrandArchetypeName';
import { SentenceLengthPreference } from '$lib/api/brands/schema/BrandToneOfVoice';
import type { BrandDataResponse } from '$lib/api/brand-data/schema/BrandData';
import { contentPillarToRequest } from '$lib/api/brand-data/schema/ContentPillar';

const DEFAULT_TONE_OF_VOICE_RAW = {
	formality_level: 1,
	humour_level: 1,
	irreverence_level: 1,
	enthusiasm_level: 1,
	industry_jargon_usage_level: 1,
	sentence_length_preference: SentenceLengthPreference.MEDIUM,
	sensory_keywords: [] as string[],
	excluded_words: [] as string[],
	signature_words: [] as string[]
};

export interface BrandGenerationJobAcceptRequest {
	name: string;
	data: BrandDataResponse;
}

export function buildAcceptRequest(
	name: string,
	formData: BrandSettingsFormData
): BrandGenerationJobAcceptRequest {
	return {
		name,
		data: {
			logo_url: formData.logoUrl,
			media_urls: formData.mediaUrls,
			colors: formData.colors,
			brand_mission: formData.brandMission,
			archetype: (formData.archetype || null) as BrandArchetypeName | null,
			locale: formData.locale,
			audiences: formData.audiences.map(audienceToRequest),
			content_pillars: formData.contentPillars.map(contentPillarToRequest),
			tone_of_voice: formData.toneOfVoice ?? DEFAULT_TONE_OF_VOICE_RAW,
			positioning: {
				description: formData.description,
				points_of_parity: formData.positioningPointsOfParity,
				points_of_difference: formData.positioningPointsOfDifference,
				product_description: formData.productDescription
			}
		}
	};
}
