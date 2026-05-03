<script lang="ts">
	import { useBrandEditorStore } from './BrandEditorStore.svelte';
	import { createDefaultContentPillar } from './form-data';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Megaphone, Plus } from 'lucide-svelte';
	import ContentPillarCard from '$lib/components/brand/settings/content-pillar/ContentPillarCard.svelte';
	import ContentPillarEditDialog from '$lib/components/brand/settings/content-pillar/ContentPillarEditDialog.svelte';

	interface Props {
		readonly?: boolean;
	}

	let { readonly = false }: Props = $props();

	const store = useBrandEditorStore();

	let showPillarModal = $state(false);
	let editingPillarIndex = $state<number | null>(null);

	function addPillar() {
		if (readonly) return;
		store.contentPillars = [...store.contentPillars, createDefaultContentPillar()];
		editingPillarIndex = store.contentPillars.length - 1;
		showPillarModal = true;
	}

	function editPillar(index: number) {
		if (readonly) return;
		editingPillarIndex = index;
		showPillarModal = true;
	}

	function removePillar(index: number) {
		if (readonly) return;
		store.contentPillars = store.contentPillars.filter((_, i) => i !== index);
		editingPillarIndex = null;
	}
</script>

<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80">
	<CardContent class="p-6">
		<div class="mb-4 flex items-center justify-between">
			<h3 class="text-lg font-semibold flex items-center gap-2">
				<Megaphone class="h-5 w-5 text-orange-600" />
				Content Pillars
			</h3>
			<Button type="button" variant="ghost" size="sm" onclick={addPillar} disabled={readonly}>
				<Plus class="h-4 w-4 mr-1" />
				Add pillar
			</Button>
		</div>
		{#if store.contentPillars.length > 0}
			<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
				{#each store.contentPillars as pillar, index (pillar.id)}
					<div class="min-w-[260px]">
						<ContentPillarCard
							{pillar}
							audiences={store.audiences}
							{readonly}
							onEditRequested={() => editPillar(index)}
						/>
					</div>
				{/each}
			</div>
		{:else if !readonly}
			<p class="text-muted-foreground italic text-sm">No pillars yet. Add one above.</p>
		{:else}
			<p class="text-muted-foreground italic text-sm">No pillars yet.</p>
		{/if}
	</CardContent>
</Card>

{#if showPillarModal && editingPillarIndex !== null && store.contentPillars[editingPillarIndex]}
	<ContentPillarEditDialog
		bind:open={showPillarModal}
		bind:pillar={store.contentPillars[editingPillarIndex]}
		audiences={store.audiences}
		{readonly}
		onDelete={() => {
			if (editingPillarIndex === null) return;
			removePillar(editingPillarIndex);
			editingPillarIndex = null;
		}}
	/>
{/if}
