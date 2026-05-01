<script lang="ts">
	import type { BrandSettingsFormData } from '$lib/api/brand-data/model/BrandData';
	import ContentPillarItemMarketingSetting from '$lib/components/brand_settings/ContentPillarItemMarketingSetting.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import * as Item from '$lib/components/ui/item';
	import { Label } from '$lib/components/ui/label';
	import { Plus, Truck } from 'lucide-svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
	}

	let { data = $bindable(), readonly = false }: Props = $props();
	let editingParityIndex = $state<number | null>(null);
	let editingDifferenceIndex = $state<number | null>(null);

	function addParity() {
		data.positioningPointsOfParity = [...data.positioningPointsOfParity, ''];
		editingParityIndex = data.positioningPointsOfParity.length - 1;
	}

	function saveParityAt(index: number, newValue: string) {
		const updated = [...data.positioningPointsOfParity];
		if (newValue) updated[index] = newValue;
		else updated.splice(index, 1);
		data.positioningPointsOfParity = updated;
		editingParityIndex = null;
	}

	function removeParity(index: number) {
		data.positioningPointsOfParity = data.positioningPointsOfParity.filter((_, i) => i !== index);
		if (editingParityIndex === index) editingParityIndex = null;
		else if (editingParityIndex !== null && editingParityIndex > index) editingParityIndex--;
	}

	function addDifference() {
		data.positioningPointsOfDifference = [...data.positioningPointsOfDifference, ''];
		editingDifferenceIndex = data.positioningPointsOfDifference.length - 1;
	}

	function saveDifferenceAt(index: number, newValue: string) {
		const updated = [...data.positioningPointsOfDifference];
		if (newValue) updated[index] = newValue;
		else updated.splice(index, 1);
		data.positioningPointsOfDifference = updated;
		editingDifferenceIndex = null;
	}

	function removeDifference(index: number) {
		data.positioningPointsOfDifference = data.positioningPointsOfDifference.filter(
			(_, i) => i !== index
		);
		if (editingDifferenceIndex === index) editingDifferenceIndex = null;
		else if (editingDifferenceIndex !== null && editingDifferenceIndex > index)
			editingDifferenceIndex--;
	}
	const hasPositioning = $derived(
		data.positioningPointsOfParity.length > 0 || data.positioningPointsOfDifference.length > 0
	);
	const parity = $derived(data.positioningPointsOfParity);
	const difference = $derived(data.positioningPointsOfDifference);
</script>

{#if hasPositioning}
	<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80">
		<CardContent class="p-6">
			<div class="mb-4 flex items-center justify-between">
				<h3 class="text-lg font-semibold flex items-center gap-2">
					<Truck class="h-5 w-5 text-purple-600" />
					Positioning
				</h3>
			</div>
			<div class="grid grid-cols-3 gap-4">
				<div>
					<div class="mb-2 flex items-center justify-between">
						<Label class="text-sm font-medium text-muted-foreground"
							>Points of Parity</Label
						>
						{#if !readonly}
							<Button type="button" variant="ghost" size="sm" onclick={addParity}>
								<Plus class="h-4 w-4 mr-1" />
								Add
							</Button>
						{/if}
					</div>
					{#if parity.length > 0}
						<Item.Group class="space-y-1.5">
							{#each parity as point, index (index)}
								<ContentPillarItemMarketingSetting
									pillar={point}
									{readonly}
									startInEditMode={editingParityIndex === index}
									onSave={(newValue) => saveParityAt(index, newValue)}
									onRemove={() => removeParity(index)}
								/>
							{/each}
						</Item.Group>
					{:else if !readonly}
						<p class="text-muted-foreground italic text-sm">None yet. Add one above.</p>
					{:else}
						<p class="text-muted-foreground italic text-sm">None yet.</p>
					{/if}
				</div>
				<div>
					<div class="mb-2 flex items-center justify-between">
						<Label class="text-sm font-medium text-muted-foreground"
							>Points of Difference</Label
						>
						{#if !readonly}
							<Button type="button" variant="ghost" size="sm" onclick={addDifference}>
								<Plus class="h-4 w-4 mr-1" />
								Add
							</Button>
						{/if}
					</div>
					{#if difference.length > 0}
						<Item.Group class="space-y-1.5">
							{#each difference as point, index (index)}
								<ContentPillarItemMarketingSetting
									pillar={point}
									{readonly}
									startInEditMode={editingDifferenceIndex === index}
									onSave={(newValue) => saveDifferenceAt(index, newValue)}
									onRemove={() => removeDifference(index)}
								/>
							{/each}
						</Item.Group>
					{:else if !readonly}
						<p class="text-muted-foreground italic text-sm">None yet. Add one above.</p>
					{:else}
						<p class="text-muted-foreground italic text-sm">None yet.</p>
					{/if}
				</div>
			</div>
		</CardContent>
	</Card>
{:else if !readonly}
	<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80">
		<CardContent class="p-6">
			<div class="mb-4 flex items-center justify-between">
				<h3 class="text-lg font-semibold flex items-center gap-2">
					<Truck class="h-5 w-5 text-purple-600" />
					Positioning
				</h3>
			</div>
			<p class="text-muted-foreground italic">No positioning settings yet.</p>
		</CardContent>
	</Card>
{/if}
