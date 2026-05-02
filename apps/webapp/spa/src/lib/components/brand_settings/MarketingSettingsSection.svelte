<script lang="ts">
	import { createDefaultContentPillar, type BrandSettingsFormData } from './form-data';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Megaphone, Plus } from 'lucide-svelte';
	import ContentPillarCard from '$lib/components/brand_settings/content-pillar/ContentPillarCard.svelte';
	import ContentPillarEditDialog from '$lib/components/brand_settings/content-pillar/ContentPillarEditDialog.svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
	}

	let { data = $bindable(), readonly = false }: Props = $props();
	let showPillarModal = $state(false);
	let editingPillarIndex = $state<number | null>(null);

	function addPillar() {
		if (readonly) return;
		data.contentPillars = [...data.contentPillars, createDefaultContentPillar()];
		editingPillarIndex = data.contentPillars.length - 1;
		showPillarModal = true;
	}

	function editPillar(index: number) {
		if (readonly) return;
		editingPillarIndex = index;
		showPillarModal = true;
	}

	function removePillar(index: number) {
		if (readonly) return;
		data.contentPillars = data.contentPillars.filter((_, i) => i !== index);
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
		{#if data.contentPillars.length > 0}
			<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
				{#each data.contentPillars as pillar, index (pillar.id)}
					<div class="min-w-[260px]">
						<ContentPillarCard
							{pillar}
							audiences={data.audiences}
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

{#if showPillarModal && editingPillarIndex !== null && data.contentPillars[editingPillarIndex]}
	<ContentPillarEditDialog
		bind:open={showPillarModal}
		bind:pillar={data.contentPillars[editingPillarIndex]}
		audiences={data.audiences}
		{readonly}
		onDelete={() => {
			if (editingPillarIndex === null) return;
			removePillar(editingPillarIndex);
			editingPillarIndex = null;
		}}
	/>
{/if}
