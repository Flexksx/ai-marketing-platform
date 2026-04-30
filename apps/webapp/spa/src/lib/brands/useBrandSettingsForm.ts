import type { BrandResponse, UpdateBrandRequest } from "@ai-marketing-platform/platform-api-client";
import { computed, reactive, watch } from "vue";
import type { Ref } from "vue";

export interface AudienceFormItem {
	id?: string;
	name: string;
	funnel_stage: "TOFU" | "MOFU" | "BOFU" | "";
	desires: string[];
	pain_points: string[];
}

export interface PillarFormItem {
	id?: string;
	name: string;
	topic: string;
	funnel_stage: "TOFU" | "MOFU" | "BOFU" | "";
	content_type_indicators: string[];
}

export interface BrandFormState {
	name: string;
	website_url: string;
	description: string;
	target_audiences: AudienceFormItem[];
	content_pillars: PillarFormItem[];
}

const emptyForm = (): BrandFormState => ({
	name: "",
	website_url: "",
	description: "",
	target_audiences: [],
	content_pillars: [],
});

const brandToForm = (brand: BrandResponse): BrandFormState => ({
	name: brand.name ?? "",
	website_url: brand.data?.website_url ?? "",
	description: brand.data?.description ?? "",
	target_audiences: (brand.data?.target_audiences ?? []).map((a) => ({
		id: a.id,
		name: a.name ?? "",
		funnel_stage: (a.funnel_stage as "TOFU" | "MOFU" | "BOFU") ?? "",
		desires: [...(a.desires ?? [])],
		pain_points: [...(a.pain_points ?? [])],
	})),
	content_pillars: (brand.data?.content_pillars ?? []).map((p) => ({
		id: p.id,
		name: p.name ?? "",
		topic: p.topic ?? "",
		funnel_stage: (p.funnel_stage as "TOFU" | "MOFU" | "BOFU") ?? "",
		content_type_indicators: [...(p.content_type_indicators ?? [])],
	})),
});

const formToRequest = (form: BrandFormState): UpdateBrandRequest => ({
	name: form.name || undefined,
	website_url: form.website_url || undefined,
	description: form.description || undefined,
	target_audiences: form.target_audiences.map((a) => ({
		name: a.name || undefined,
		funnel_stage: (a.funnel_stage || undefined) as "TOFU" | "MOFU" | "BOFU" | undefined,
		desires: a.desires.filter(Boolean),
		pain_points: a.pain_points.filter(Boolean),
	})),
	content_pillars: form.content_pillars.map((p) => ({
		name: p.name || undefined,
		topic: p.topic || undefined,
		funnel_stage: (p.funnel_stage || undefined) as "TOFU" | "MOFU" | "BOFU" | undefined,
		content_type_indicators: p.content_type_indicators.filter(Boolean),
	})),
});

export const useBrandSettingsForm = (brand: Ref<BrandResponse | undefined>) => {
	const form = reactive<BrandFormState>(emptyForm());
	let serverSnapshot = "";

	const syncFromBrand = (b: BrandResponse) => {
		const fresh = brandToForm(b);
		serverSnapshot = JSON.stringify(fresh);
		Object.assign(form, fresh);
	};

	watch(
		brand,
		(b) => {
			if (b) {
				syncFromBrand(b);
			}
		},
		{ immediate: true },
	);

	const isDirty = computed(() => {
		if (!serverSnapshot) return false;
		return JSON.stringify(form) !== serverSnapshot;
	});

	const discard = () => {
		if (brand.value) {
			syncFromBrand(brand.value);
		}
	};

	const toRequest = (): UpdateBrandRequest => formToRequest(form);

	return { form, isDirty, discard, toRequest };
};
