import type { BrandData } from '$lib/api/generated/models/BrandData';
import type { BrandToneOfVoice } from '$lib/api/generated/models/BrandToneOfVoice';
import type { ContentPillar } from '$lib/api/generated/models/ContentPillar';

export interface BrandSettingsFormData {
	name: string;
	data: BrandData;
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
		data: {
			logoUrl: null,
			brandMission: null,
			locale: null,
			colors: [],
			mediaUrls: [],
			audiences: [],
			contentPillars: [],
			toneOfVoice: { ...defaultToneOfVoice },
			positioning: {
				description: '',
				pointsOfParity: [],
				pointsOfDifference: [],
				productDescription: ''
			}
		},
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
