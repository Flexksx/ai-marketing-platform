<script lang="ts">
	import { useAcceptBrandGenerationJob } from '$lib/resources/brand-generation-jobs/mutations';
	import { navigate } from '$lib/navigation';
	import type { BrandResponse } from '$lib/api/generated/models/BrandResponse';
	import type { BrandGenerationJobAcceptRequest } from '$lib/api/generated/models/BrandGenerationJobAcceptRequest';
	import {
		AudienceSettingsSection,
		BrandColorsSection,
		BrandImagesSection,
		GeneralSettingsSection,
		MarketingSettingsSection,
		ToneOfVoiceSection,
		createEmptyBrandSettingsFormData,
		type BrandSettingsFormData
	} from '$lib/components/brand_settings';
	import { Button } from '$lib/components/ui/button';
	import { CheckCircle2, Loader2 } from 'lucide-svelte';
	import { fade } from 'svelte/transition';

	type Props = {
		jobId: string;
		brandData: { name: string; data: BrandResponse['data'] } | null;
		onClose: () => void;
		onGenerateAnother: () => void;
	};

	let { jobId, brandData, onClose, onGenerateAnother }: Props = $props();

	const acceptJobMutation = useAcceptBrandGenerationJob();

	let formData = $state<BrandSettingsFormData>(createEmptyBrandSettingsFormData());

	$effect(() => {
		if (!brandData) return;

		formData = {
			name: brandData.name ?? '',
			logoUrl: brandData.data?.logoUrl ?? '',
			description: brandData.data?.positioning?.description ?? '',
			brandMission: brandData.data?.brandMission ?? '',
			locale: brandData.data?.locale ?? null,
			colors: brandData.data?.colors ?? [],
			mediaUrls: brandData.data?.mediaUrls ?? [],
			audiences: brandData.data?.audiences ?? [],
			contentPillars: brandData.data?.contentPillars ? [...brandData.data.contentPillars] : [],
			toneOfVoice: brandData.data?.toneOfVoice ?? {
				archetype: null,
				jargonDensity: 1,
				visualDensity: 1,
				mustUseWords: [],
				forbiddenWords: []
			},
			positioningPointsOfParity: brandData.data?.positioning?.pointsOfParity ?? [],
			positioningPointsOfDifference: brandData.data?.positioning?.pointsOfDifference ?? [],
			productDescription: brandData.data?.positioning?.productDescription ?? '',
			pendingLogoFile: null
		};
	});

	function handleSave() {
		if (!jobId) return;

		const body: BrandGenerationJobAcceptRequest = {
			name: formData.name,
			data: {
				logoUrl: formData.logoUrl || null,
				mediaUrls: formData.mediaUrls,
				colors: formData.colors,
				brandMission: formData.brandMission || null,
				locale: formData.locale,
				audiences: formData.audiences,
				contentPillars: formData.contentPillars,
				toneOfVoice: formData.toneOfVoice,
				positioning: {
					description: formData.description,
					pointsOfParity: formData.positioningPointsOfParity,
					pointsOfDifference: formData.positioningPointsOfDifference,
					productDescription: formData.productDescription
				}
			}
		};

		acceptJobMutation.mutate(
			{ jobId, body },
			{
				onSuccess: (brand) => {
					navigate(`/brands/${brand.id}/posts_calendar?onboarded=true`);
				}
			}
		);
	}
</script>

<div class="flex flex-col gap-6">
	<div class="mb-4">
		<div class="flex items-center gap-4 mb-2">
			<CheckCircle2 class="w-8 h-8 text-green-500" />
			<div>
				<h1 class="text-3xl font-bold">Review Your Brand</h1>
				<p class="text-muted-foreground" style="font-family: var(--font-body);">
					Review and edit the extracted brand information before saving
				</p>
			</div>
		</div>
	</div>

	<div
		class="overflow-y-auto overflow-x-hidden px-1"
		transition:fade={{ duration: 300 }}
	>
		<div class="grid grid-cols-2 gap-4 auto-rows-min pb-4">
			<div>
				<GeneralSettingsSection data={formData} readonly={false} />
			</div>

			{#if formData.mediaUrls.length > 0}
				<div class="row-span-2">
					<BrandImagesSection data={formData} readonly={false} />
				</div>
			{/if}

			<div>
				<BrandColorsSection data={formData} readonly={false} />
			</div>

			<div class="col-span-2">
				<MarketingSettingsSection data={formData} readonly={false} />
			</div>

			<div class="col-span-2">
				<AudienceSettingsSection data={formData} readonly={false} />
			</div>

			<div class="col-span-2">
				<ToneOfVoiceSection data={formData} readonly={false} />
			</div>
		</div>
	</div>

	{#if acceptJobMutation.error}
		<div class="shrink-0 rounded-lg border border-red-200 bg-red-50 p-3 dark:border-red-800 dark:bg-red-900/20">
			<p class="text-sm text-red-600 dark:text-red-200">
				{acceptJobMutation.error instanceof Error
					? acceptJobMutation.error.message
					: 'Failed to save brand'}
			</p>
		</div>
	{/if}

	<div class="flex shrink-0 gap-6 pt-8 pb-4 justify-center">
		<Button variant="outline" size="lg" onclick={onGenerateAnother} disabled={acceptJobMutation.isPending} class="px-8 h-12 text-base">
			Discard
		</Button>
		<Button
			size="lg"
			onclick={handleSave}
			disabled={acceptJobMutation.isPending || !jobId}
			class="bg-blue-600 hover:bg-blue-700 px-16 h-14 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
		>
			{#if acceptJobMutation.isPending}
				<Loader2 class="mr-2 h-5 w-5 animate-spin" />
				Saving...
			{:else}
				Save Brand
			{/if}
		</Button>
	</div>
</div>
