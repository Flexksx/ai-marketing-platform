import type { BrandArchetypeName } from './BrandArchetypeName';
import type { BrandAudienceResponse } from './BrandAudience';
import type { BrandColor } from './BrandColor';
import type { BrandToneOfVoice } from './BrandToneOfVoice';
import type { ContentPillarResponse } from '$lib/api/brand-data/schema/ContentPillar';
import type { PositioningBrandDataResponse } from '$lib/api/brand-data/schema/PositioningBrandData';

export interface BrandDataUpdateRequest {
	logo_url?: string | null;
	media_urls?: string[] | null;
	colors?: BrandColor[] | null;
	brand_mission?: string | null;
	archetype?: BrandArchetypeName | null;
	locale?: string | null;
	audiences?: BrandAudienceResponse[] | null;
	content_pillars?: ContentPillarResponse[] | null;
	tone_of_voice?: BrandToneOfVoice | null;
	positioning?: PositioningBrandDataResponse | null;
}
