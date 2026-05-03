<script lang="ts">
	import type { BrandAudience } from '$lib/api/generated/models/BrandAudience';
	import { useBrandEditorStore } from './BrandEditorStore.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Users, Plus } from 'lucide-svelte';
	import AudienceCard from '$lib/components/brand_settings/audience/AudienceCard.svelte';
	import AudienceEditDialog from '$lib/components/brand_settings/audience/AudienceEditDialog.svelte';

	interface Props {
		readonly?: boolean;
	}

	let { readonly = false }: Props = $props();

	const store = useBrandEditorStore();

	let showAudienceModal = $state(false);
	let editingAudienceIndex = $state<number | null>(null);

	function addAudience() {
		if (readonly) return;
		const newAudience: BrandAudience = {
			id: '',
			name: '',
			ageRange: 'ANY',
			gender: 'ANY',
			incomeRange: 'ANY',
			painPoints: [],
			objections: [],
			channels: []
		};
		store.audiences = [...store.audiences, newAudience];
		editingAudienceIndex = store.audiences.length - 1;
		showAudienceModal = true;
	}

	function removeAudience(index: number) {
		if (readonly) return;
		store.audiences = store.audiences.filter((_, i) => i !== index);
	}

	function editAudience(index: number) {
		if (readonly) return;
		editingAudienceIndex = index;
		showAudienceModal = true;
	}
</script>

<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80 h-full">
	<CardContent class="p-6">
		<div class="mb-4 flex items-center justify-between">
			<h3 class="text-lg font-semibold flex items-center gap-2">
				<Users class="h-5 w-5 text-blue-600" />
				Audiences
			</h3>
			<Button type="button" variant="ghost" size="sm" onclick={addAudience} disabled={readonly}>
				<Plus class="h-4 w-4 mr-1" />
				Add audience
			</Button>
		</div>
		<div>
			{#if store.audiences.length > 0}
				<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
					{#each store.audiences as audience, index (index)}
						<div class="min-w-[260px]">
							<AudienceCard
								bind:audience={store.audiences[index]}
								{readonly}
								onEditRequested={() => editAudience(index)}
							/>
						</div>
					{/each}
				</div>
			{:else}
				<p class="text-muted-foreground italic">No audiences yet...</p>
			{/if}
		</div>
	</CardContent>
</Card>

{#if showAudienceModal && editingAudienceIndex !== null && store.audiences[editingAudienceIndex]}
	<AudienceEditDialog
		bind:open={showAudienceModal}
		bind:audience={store.audiences[editingAudienceIndex]}
		{readonly}
		onDelete={() => {
			if (editingAudienceIndex === null) return;
			removeAudience(editingAudienceIndex);
			editingAudienceIndex = null;
		}}
	/>
{/if}
