<script lang="ts">
	import { page } from '$app/state';
	import { useBrand, } from '$lib/resources/brands/queries';
	import { useDeleteBrand, useUpdateBrand } from '$lib/resources/brands/mutations';
	import { useQueryClient } from '@tanstack/svelte-query';
	import type { BrandData } from '$lib/api/generated/models/BrandData';
	import type { BrandAudience } from '$lib/api/generated/models/BrandAudience';
	import type { ContentPillar } from '$lib/api/generated/models/ContentPillar';
	import {
		AudienceSettingsSection,
		BrandImagesSection,
		GeneralSettingsSection,
		MarketingSettingsSection,
		ToneOfVoiceSection,
		createEmptyBrandSettingsFormData,
		type BrandSettingsFormData
	} from '$lib/components/brand_settings';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { ArrowLeft, Building2, LoaderCircle, Save, X } from 'lucide-svelte';
	import BrandDangerZone from './BrandDangerZone.svelte';

	const brandId = $derived(page.params.id);
	const brandQuery = useBrand(() => brandId);

	const queryClient = useQueryClient();
	const updateBrandMutation = useUpdateBrand();
	const deleteBrandMutation = useDeleteBrand();

	let brand = $derived(brandQuery?.data ?? null);
	let isLoading = $derived(brandQuery?.isLoading ?? false);
	let error = $derived(brandQuery?.error?.message ?? null);

	let formData = $state<BrandSettingsFormData>(createEmptyBrandSettingsFormData());
	let originalFormData = $state<BrandSettingsFormData>(createEmptyBrandSettingsFormData());

	$effect(() => {
		if (brand) {
			const next: BrandSettingsFormData = {
				name: brand.name ?? '',
				logoUrl: brand.data?.logoUrl ?? '',
				description: brand.data?.positioning?.description ?? '',
				brandMission: brand.data?.brandMission ?? '',
				locale: brand.data?.locale ?? null,
				colors: brand.data?.colors ? [...brand.data.colors] : [],
				mediaUrls: brand.data?.mediaUrls ? [...brand.data.mediaUrls] : [],
				audiences: brand.data?.audiences ? [...brand.data.audiences] : [],
				contentPillars: brand.data?.contentPillars ? [...brand.data.contentPillars] : [],
				toneOfVoice: brand.data?.toneOfVoice ?? {
					archetype: null,
					jargonDensity: 1,
					visualDensity: 1,
					mustUseWords: [],
					forbiddenWords: []
				},
				positioningPointsOfParity: brand.data?.positioning?.pointsOfParity ?? [],
				positioningPointsOfDifference: brand.data?.positioning?.pointsOfDifference ?? [],
				productDescription: brand.data?.positioning?.productDescription ?? '',
				pendingLogoFile: null
			};
			formData = next;
			originalFormData = JSON.parse(JSON.stringify(next));
		}
	});

	const isDirty = $derived(
		JSON.stringify({ ...formData, pendingLogoFile: null }) !== JSON.stringify(originalFormData)
		|| formData.pendingLogoFile !== null
	);

	function discardChanges() {
		formData = { ...JSON.parse(JSON.stringify(originalFormData)), pendingLogoFile: null };
	}

	let showDeleteModal = $state(false);

	const handleUpdate = async () => {
		const data: BrandData = {
			logoUrl: formData.logoUrl || null,
			mediaUrls: formData.mediaUrls,
			colors: formData.colors,
			brandMission: formData.brandMission || null,
			locale: formData.locale,
			audiences: formData.audiences as BrandAudience[],
			contentPillars: formData.contentPillars as ContentPillar[],
			toneOfVoice: formData.toneOfVoice,
			positioning: {
				description: formData.description,
				pointsOfParity: formData.positioningPointsOfParity,
				pointsOfDifference: formData.positioningPointsOfDifference,
				productDescription: formData.productDescription
			}
		};

		await updateBrandMutation.mutateAsync({
			brandId,
			name: formData.name,
			data,
			logoFile: formData.pendingLogoFile ?? undefined
		});
	};

	const handleDelete = async () => {
		await deleteBrandMutation.mutateAsync(brandId);
	};
</script>

<div class="container mx-auto px-4 py-8">
	{#if isLoading}
		<div class="flex items-center justify-center py-12">
			<LoaderCircle class="h-8 w-8 animate-spin text-muted-foreground" />
		</div>
	{:else if error || !brand}
		<div class="flex flex-col items-center justify-center py-24 text-center">
			<div class="text-6xl mb-4">😢</div>
			<h1 class="text-3xl font-bold mb-2">Brand Not Found</h1>
			<p class="text-muted-foreground mb-6">
				The brand you're looking for doesn't exist or has been removed.
			</p>
			<Button href="/brands" variant="outline">
				<ArrowLeft class="h-4 w-4 mr-2" /> Back to Brands
			</Button>
		</div>
	{:else if brand}
		<form
			onsubmit={(e) => {
				e.preventDefault();
				handleUpdate();
			}}
		>
			<div class="flex flex-col gap-6">
				<div class="mb-4">
					<div class="flex items-center gap-4 mb-2">
						<Building2 class="w-8 h-8 text-primary" />
						<div>
							<h1 class="text-3xl font-bold">Brand Settings</h1>
							<p class="text-muted-foreground">Manage your brand identity and settings</p>
						</div>
					</div>
				</div>

				<div
					class="overflow-y-auto overflow-x-hidden px-1 {isDirty ? 'pb-24' : ''}"
				>
				<div class="grid grid-cols-2 gap-4 auto-rows-min pb-4">
					<div>
						<GeneralSettingsSection bind:data={formData} readonly={false} />
					</div>

					{#if formData.mediaUrls.length > 0}
						<div class="row-span-2">
							<BrandImagesSection bind:data={formData} readonly={false} />
						</div>
					{/if}

					<div class="col-span-2">
						<MarketingSettingsSection bind:data={formData} readonly={false} />
					</div>

					<div class="col-span-2">
						<AudienceSettingsSection bind:data={formData} readonly={false} />
					</div>

					<div class="col-span-2">
						<ToneOfVoiceSection bind:data={formData} readonly={false} />
					</div>
				</div>
				</div>

				{#if isDirty}
					<div
						class="fixed bottom-0 left-0 right-0 z-50 border-t bg-background px-4 py-3 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] dark:shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.3)]"
					>
						<div class="container mx-auto flex justify-end gap-3">
							<Button
								type="button"
								variant="outline"
								size="lg"
								onclick={discardChanges}
							>
								<X class="h-4 w-4 mr-2" />
								Discard
							</Button>
							<Button
								type="submit"
								size="lg"
								disabled={updateBrandMutation.isPending}
								class="bg-blue-600 hover:bg-blue-700 px-6"
							>
								{#if updateBrandMutation.isPending}
									<LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
									Saving...
								{:else}
									<Save class="h-4 w-4 mr-2" />
									Save changes
								{/if}
							</Button>
						</div>
					</div>
				{/if}

				<div class="mt-12">
					<BrandDangerZone onDeleteClick={() => (showDeleteModal = true)} />
				</div>
			</div>
		</form>
	{/if}
</div>

<Dialog.Root bind:open={showDeleteModal}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Delete Brand?</Dialog.Title>
			<Dialog.Description>Irreversible.</Dialog.Description>
		</Dialog.Header>
		<Dialog.Footer>
			<Button variant="outline" onclick={() => (showDeleteModal = false)}>Cancel</Button>
			<Button variant="destructive" onclick={handleDelete}>Delete Permanently</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
