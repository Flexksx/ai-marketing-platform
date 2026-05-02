import type { BrandAudience } from '$lib/api/generated/models/BrandAudience';
import type { BrandColor } from '$lib/api/generated/models/BrandColor';
import type { BrandToneOfVoice } from '$lib/api/generated/models/BrandToneOfVoice';
import type { ContentPillar } from '$lib/api/generated/models/ContentPillar';

export interface BrandSettingsFormData {
	name: string;
	logoUrl: string;
	description: string;
	brandMission: string;
	locale: string | null;
	colors: BrandColor[];
	mediaUrls: string[];
	audiences: BrandAudience[];
	contentPillars: ContentPillar[];
	toneOfVoice: BrandToneOfVoice;
	positioningPointsOfParity: string[];
	positioningPointsOfDifference: string[];
	productDescription: string;
	pendingLogoFile: File | null;
}

export const defaultToneOfVoice: BrandToneOfVoice = {
	archetype: null,
	jargonDensity: 1,
	visualDensity: 1,
	mustUseWords: [],
	forbiddenWords: []
};

export function createEmptyBrandSettingsFormData(): BrandSettingsFormData {
	return {
		name: '',
		logoUrl: '',
		description: '',
		brandMission: '',
		locale: null,
		colors: [],
		mediaUrls: [],
		audiences: [],
		contentPillars: [],
		toneOfVoice: { ...defaultToneOfVoice },
		positioningPointsOfParity: [],
		positioningPointsOfDifference: [],
		productDescription: '',
		pendingLogoFile: null
	};
}

export function createDefaultContentPillar(): ContentPillar {
	return {
		id: crypto.randomUUID(),
		name: '',
		businessGoal: 'BUILD_TRUST',
		type: 'THOUGHT_LEADERSHIP',
		funnelStage: 'LOYALTY',
		contentTypes: [],
		audienceIds: [],
		hooks: [],
		callsToAction: []
	};
}
