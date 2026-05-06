import type { BrandArchetypeName } from '$lib/api/brands/schema/BrandArchetypeName';
import type { BrandAudienceResponse } from '$lib/api/brands/schema/BrandAudience';
import type { BrandColor } from '$lib/api/brands/schema/BrandColor';
import type { BrandToneOfVoice } from '$lib/api/brands/schema/BrandToneOfVoice';
import type { ContentPillarResponse } from './ContentPillar';
import type { PositioningBrandDataResponse } from './PositioningBrandData';

export interface BrandDataResponse {
	logo_url?: string | null;
	media_urls: string[];
	colors: BrandColor[];
	brand_mission?: string | null;
	archetype?: BrandArchetypeName | null;
	locale?: string | null;
	audiences: BrandAudienceResponse[];
	content_pillars: ContentPillarResponse[];
	tone_of_voice: BrandToneOfVoice;
	positioning: PositioningBrandDataResponse;
}
