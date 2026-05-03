import type { BrandToneOfVoice } from '$lib/api/generated/models/BrandToneOfVoice';
import type { ContentPillar } from '$lib/api/generated/models/ContentPillar';

export const defaultToneOfVoice: BrandToneOfVoice = {
	archetype: null,
	jargonDensity: 1,
	visualDensity: 1,
	mustUseWords: [],
	forbiddenWords: []
};

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
