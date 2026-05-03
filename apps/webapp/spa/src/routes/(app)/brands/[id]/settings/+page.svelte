<script lang="ts">
	import { page } from '$app/state';
	import { useBrand } from '$lib/resources/brands/queries';
	import { useDeleteBrand, useUpdateBrand } from '$lib/resources/brands/mutations';
	import { useQueryClient } from '@tanstack/svelte-query';
	import { BrandsApi } from '$lib/api/generated/apis/BrandsApi';
	import { openApiConfiguration } from '$lib/backend/generated-client';
	import { queryKeys } from '$lib/resources/queryKeys';
	import {
		AudienceSettingsSection,
		BrandImagesSection,
		GeneralSettingsSection,
		MarketingSettingsSection,
		ToneOfVoiceSection
	} from '$lib/components/brand_settings';
	import { setBrandEditorStore } from '$lib/components/brand_settings/BrandEditorStore.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { ArrowLeft, Building2, LoaderCircle, Save, X } from 'lucide-svelte';
	import BrandDangerZone from './BrandDangerZone.svelte';

	const brandId = $derived(page.params.id);
	const brandQuery = useBrand(() => brandId);
	const queryClient = useQueryClient();
	const api = new BrandsApi(openApiConfiguration);

	const store = setBrandEditorStore();

	// brandQuery.data is synchronously available from cache (prefetched in +page.ts load fn)
	if (brandQuery.data) store.initFromBrand(brandQuery.data);

	const updateBrandMutation = useUpdateBrand();
	const deleteBrandMutation = useDeleteBrand();

	const isDirty = $derived(store.isDirty);

	let showDeleteModal = $state(false);

	const handleUpdate = async () => {
		await updateBrandMutation.mutateAsync({ brandId, ...store.buildSavePayload() });
		const fresh = await queryClient.fetchQuery({
			queryKey: queryKeys.brand(brandId),
			queryFn: () => api.brandsGet({ brandId })
		});
		store.initFromBrand(fresh);
	};

	const handleDelete = async () => {
		await deleteBrandMutation.mutateAsync(brandId);
	};
</script>

<div class="container mx-auto px-4 py-8">
	{#if brandQuery.isLoading}
		<div class="flex items-center justify-center py-12">
			<LoaderCircle class="h-8 w-8 animate-spin text-muted-foreground" />
		</div>
	{:else if brandQuery.error || !brandQuery.data}
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
	{:else}
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

				<div class="overflow-y-auto overflow-x-hidden px-1 {isDirty ? 'pb-24' : ''}">
					<div class="grid grid-cols-2 gap-4 auto-rows-min pb-4">
						<div>
							<GeneralSettingsSection readonly={false} />
						</div>

						{#if store.mediaUrls.length > 0}
							<div class="row-span-2">
								<BrandImagesSection readonly={false} />
							</div>
						{/if}

						<div class="col-span-2">
							<MarketingSettingsSection readonly={false} />
						</div>

						<div class="col-span-2">
							<AudienceSettingsSection readonly={false} />
						</div>

						<div class="col-span-2">
							<ToneOfVoiceSection readonly={false} />
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
								onclick={() => store.discard()}
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
