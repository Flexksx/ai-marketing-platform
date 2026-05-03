import type { BrandData } from '$lib/api/generated/models/BrandData';
import type { BrandAudience } from '$lib/api/generated/models/BrandAudience';
import type { BrandColor } from '$lib/api/generated/models/BrandColor';
import type { BrandToneOfVoice } from '$lib/api/generated/models/BrandToneOfVoice';
import type { ContentPillar } from '$lib/api/generated/models/ContentPillar';
import type { PositioningBrandData } from '$lib/api/generated/models/PositioningBrandData';
import { defaultToneOfVoice } from './form-data';
import { getContext, setContext } from 'svelte';

const BRAND_EDITOR_KEY = Symbol('BrandEditor');

export class BrandEditorStore {
	name = $state('');
	logoUrl = $state<string | null>(null);
	brandMission = $state<string | null>(null);
	locale = $state<string | null>(null);
	colors = $state<BrandColor[]>([]);
	mediaUrls = $state<string[]>([]);
	audiences = $state<BrandAudience[]>([]);
	contentPillars = $state<ContentPillar[]>([]);
	toneOfVoice = $state<BrandToneOfVoice>({ ...defaultToneOfVoice });
	positioning = $state<PositioningBrandData>({
		description: '',
		pointsOfParity: [],
		pointsOfDifference: [],
		productDescription: ''
	});
	pendingLogoFile = $state<File | null>(null);

	#snapshot = $state('');

	readonly isDirty = $derived.by(
		() =>
			JSON.stringify({
				name: this.name,
				brandMission: this.brandMission,
				locale: this.locale,
				colors: this.colors,
				audiences: this.audiences,
				contentPillars: this.contentPillars,
				toneOfVoice: this.toneOfVoice,
				positioning: this.positioning
			}) !== this.#snapshot || this.pendingLogoFile !== null
	);

	initFromBrand(brand: { name: string; data?: BrandData | null }) {
		this.name = brand.name ?? '';
		this.logoUrl = brand.data?.logoUrl ?? null;
		this.brandMission = brand.data?.brandMission ?? null;
		this.locale = brand.data?.locale ?? null;
		this.colors = [...(brand.data?.colors ?? [])];
		this.mediaUrls = [...(brand.data?.mediaUrls ?? [])];
		this.audiences = [...(brand.data?.audiences ?? [])];
		this.contentPillars = [...(brand.data?.contentPillars ?? [])];
		this.toneOfVoice = { ...(brand.data?.toneOfVoice ?? defaultToneOfVoice) };
		this.positioning = {
			description: brand.data?.positioning?.description ?? '',
			pointsOfParity: [...(brand.data?.positioning?.pointsOfParity ?? [])],
			pointsOfDifference: [...(brand.data?.positioning?.pointsOfDifference ?? [])],
			productDescription: brand.data?.positioning?.productDescription ?? ''
		};
		this.pendingLogoFile = null;
		this.#snapshot = this.#buildSnapshot();
	}

	discard() {
		const original = JSON.parse(this.#snapshot);
		this.name = original.name;
		this.brandMission = original.brandMission;
		this.locale = original.locale;
		this.colors = original.colors;
		this.audiences = original.audiences;
		this.contentPillars = original.contentPillars;
		this.toneOfVoice = original.toneOfVoice;
		this.positioning = original.positioning;
		this.pendingLogoFile = null;
	}

	buildSavePayload(): { name: string; data: BrandData; logoFile?: File } {
		return {
			name: this.name,
			data: {
				logoUrl: this.logoUrl,
				brandMission: this.brandMission,
				locale: this.locale,
				colors: this.colors,
				mediaUrls: this.mediaUrls,
				audiences: this.audiences,
				contentPillars: this.contentPillars,
				toneOfVoice: this.toneOfVoice,
				positioning: this.positioning
			},
			logoFile: this.pendingLogoFile ?? undefined
		};
	}

	#buildSnapshot(): string {
		return JSON.stringify({
			name: this.name,
			brandMission: this.brandMission,
			locale: this.locale,
			colors: this.colors,
			audiences: this.audiences,
			contentPillars: this.contentPillars,
			toneOfVoice: this.toneOfVoice,
			positioning: this.positioning
		});
	}
}

export const setBrandEditorStore = () => setContext(BRAND_EDITOR_KEY, new BrandEditorStore());
export const useBrandEditorStore = () => getContext<BrandEditorStore>(BRAND_EDITOR_KEY);
