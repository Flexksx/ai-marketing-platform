<script lang="ts">
	import type { PositioningBrandData } from '$lib/api/generated/models/PositioningBrandData';
	import StringItemSetting from '$lib/components/brand_settings/StringItemSetting.svelte';
	import * as Item from '$lib/components/ui/item';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import { Plus } from 'lucide-svelte';

	interface Props {
		positioning: PositioningBrandData;
		readonly?: boolean;
	}

	let { positioning = $bindable(), readonly = false }: Props = $props();

	let editingParityIndex = $state<number | null>(null);
	let editingDifferenceIndex = $state<number | null>(null);

	function addParity() {
		positioning.pointsOfParity = [...(positioning.pointsOfParity ?? []), ''];
		editingParityIndex = (positioning.pointsOfParity ?? []).length - 1;
	}

	function saveParityAt(index: number, newValue: string) {
		const updated = [...(positioning.pointsOfParity ?? [])];
		if (newValue) updated[index] = newValue;
		else updated.splice(index, 1);
		positioning.pointsOfParity = updated;
		editingParityIndex = null;
	}

	function removeParity(index: number) {
		positioning.pointsOfParity = (positioning.pointsOfParity ?? []).filter((_, i) => i !== index);
		if (editingParityIndex === index) editingParityIndex = null;
		else if (editingParityIndex !== null && editingParityIndex > index) editingParityIndex--;
	}

	function addDifference() {
		positioning.pointsOfDifference = [...(positioning.pointsOfDifference ?? []), ''];
		editingDifferenceIndex = (positioning.pointsOfDifference ?? []).length - 1;
	}

	function saveDifferenceAt(index: number, newValue: string) {
		const updated = [...(positioning.pointsOfDifference ?? [])];
		if (newValue) updated[index] = newValue;
		else updated.splice(index, 1);
		positioning.pointsOfDifference = updated;
		editingDifferenceIndex = null;
	}

	function removeDifference(index: number) {
		positioning.pointsOfDifference = (positioning.pointsOfDifference ?? []).filter(
			(_, i) => i !== index
		);
		if (editingDifferenceIndex === index) editingDifferenceIndex = null;
		else if (editingDifferenceIndex !== null && editingDifferenceIndex > index)
			editingDifferenceIndex--;
	}

	const parity = $derived(positioning.pointsOfParity ?? []);
	const difference = $derived(positioning.pointsOfDifference ?? []);
</script>

<div class="mt-4 border-t border-border pt-4">
	<div class="mb-3 space-y-2">
		<div>
			<Label class="text-xs font-medium text-muted-foreground">Product description</Label>
			<p class="text-[11px] text-muted-foreground">
				In 3–5 words, what does the brand sell or provide?
			</p>
		</div>
		{#if readonly}
			<p class="text-xs">
				{#if positioning.productDescription}
					{positioning.productDescription}
				{:else}
					<span class="text-muted-foreground italic">No product description yet.</span>
				{/if}
			</p>
		{:else}
			<input
				type="text"
				class="w-full h-8 rounded-md border border-input bg-background px-2 text-xs"
				bind:value={positioning.productDescription}
				placeholder="e.g. Premium residential brokerage"
			/>
		{/if}
	</div>
	<div class="grid grid-cols-2 gap-4">
		<div>
			<div class="mb-2 flex items-center justify-between">
				<div>
					<Label class="text-xs font-medium text-muted-foreground">Core product description</Label>
					<p class="text-[11px] text-muted-foreground">
						What you offer that customers expect in your category.
					</p>
				</div>
				{#if !readonly}
					<Button type="button" variant="ghost" size="sm" class="h-7 px-2" onclick={addParity}>
						<Plus class="h-3 w-3 mr-1" />
						Add
					</Button>
				{/if}
			</div>
		{#if parity.length > 0}
			<Item.Group class="space-y-1.5">
				{#each parity as point, index (index)}
					<StringItemSetting
						value={point}
						{readonly}
						startInEditMode={editingParityIndex === index}
						placeholder="e.g. Fast delivery"
						onSave={(newValue) => saveParityAt(index, newValue)}
						onRemove={() => removeParity(index)}
					/>
				{/each}
			</Item.Group>
			{:else if !readonly}
				<p class="text-muted-foreground italic text-xs">None yet. Add one above.</p>
			{:else}
				<p class="text-muted-foreground italic text-xs">None yet.</p>
			{/if}
		</div>
		<div>
			<div class="mb-2 flex items-center justify-between">
				<div>
					<Label class="text-xs font-medium text-muted-foreground">Unique product description</Label>
					<p class="text-[11px] text-muted-foreground">
						Specific ways your offer stands out from alternatives.
					</p>
				</div>
				{#if !readonly}
					<Button
						type="button"
						variant="ghost"
						size="sm"
						class="h-7 px-2"
						onclick={addDifference}
					>
						<Plus class="h-3 w-3 mr-1" />
						Add
					</Button>
				{/if}
			</div>
		{#if difference.length > 0}
			<Item.Group class="space-y-1.5">
				{#each difference as point, index (index)}
					<StringItemSetting
						value={point}
						{readonly}
						startInEditMode={editingDifferenceIndex === index}
						placeholder="e.g. Personalized service"
						onSave={(newValue) => saveDifferenceAt(index, newValue)}
						onRemove={() => removeDifference(index)}
					/>
				{/each}
			</Item.Group>
			{:else if !readonly}
				<p class="text-muted-foreground italic text-xs">None yet. Add one above.</p>
			{:else}
				<p class="text-muted-foreground italic text-xs">None yet.</p>
			{/if}
		</div>
	</div>
</div>
