<script lang="ts">
	import type { ContentPillar } from '$lib/api/generated/models/ContentPillar';
	import type { BrandAudience } from '$lib/api/generated/models/BrandAudience';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Trash2 } from 'lucide-svelte';

	interface Props {
		pillar: ContentPillar;
		audiences: BrandAudience[];
		open?: boolean;
		readonly?: boolean;
		onDelete?: () => void;
	}

	let {
		pillar = $bindable(),
		audiences,
		open = $bindable(false),
		readonly = false,
		onDelete
	}: Props = $props();

	function updatePillar(patch: Partial<ContentPillar>) {
		if (readonly) return;
		pillar = { ...pillar, ...patch };
	}

	function toggleAudience(audienceId: string) {
		if (readonly) return;
		const current = pillar.audienceIds ?? [];
		const isLinked = current.includes(audienceId);
		updatePillar({
			audienceIds: isLinked ? current.filter((id) => id !== audienceId) : [...current, audienceId]
		});
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Content class="max-w-lg">
		<Dialog.Header>
			{#if readonly}
				<Dialog.Title>{pillar.name || 'Untitled pillar'}</Dialog.Title>
			{:else}
				<div class="flex flex-col gap-1">
					<Label class="text-xs text-muted-foreground">Pillar name</Label>
					<Input
						value={pillar.name}
						placeholder="e.g. Educational content"
						oninput={(event) => updatePillar({ name: event.currentTarget.value })}
						class="h-9"
					/>
				</div>
			{/if}
		</Dialog.Header>

		<div class="py-4 space-y-4">
			<div class="space-y-2">
				<Label>Target audiences</Label>
				{#if audiences.length > 0}
					<div class="flex flex-wrap gap-2">
						{#each audiences as audience (audience.id)}
							{@const isLinked = (pillar.audienceIds ?? []).includes(audience.id ?? '')}
							<button
								type="button"
								class="inline-flex items-center rounded-full border px-3 py-1 text-xs transition-colors
									{isLinked
									? 'bg-primary text-primary-foreground border-primary'
									: 'bg-background text-muted-foreground hover:bg-muted'}"
								onclick={() => toggleAudience(audience.id ?? '')}
								disabled={readonly}
							>
								{audience.name || 'Untitled audience'}
							</button>
						{/each}
					</div>
				{:else}
					<p class="text-xs text-muted-foreground italic">No audiences available. Add audiences first.</p>
				{/if}
			</div>
		</div>

		<Dialog.Footer>
			<div class="flex w-full items-center justify-between">
				{#if !readonly && onDelete}
					<Button
						type="button"
						variant="ghost"
						class="text-destructive hover:bg-destructive/5 cursor-pointer rounded-full"
						onclick={() => {
							onDelete();
							open = false;
						}}
					>
						<Trash2 class="mr-2 h-4 w-4" />
						Delete
					</Button>
				{/if}
				<Button type="button" variant="outline" class="ml-auto" onclick={() => (open = false)}>
					Done
				</Button>
			</div>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
