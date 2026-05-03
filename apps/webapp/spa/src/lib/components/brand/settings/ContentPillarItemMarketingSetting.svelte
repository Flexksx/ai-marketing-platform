<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Item from '$lib/components/ui/item';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Pencil, Trash2 } from 'lucide-svelte';

	interface Props {
		pillar: string;
		readonly?: boolean;
		startInEditMode?: boolean;
		onSave: (updated: string) => void;
		onRemove: () => void;
	}

	let { pillar, readonly = false, startInEditMode = false, onSave, onRemove }: Props = $props();
	let isEditing = $state(false);
	let editValue = $state('');

	$effect(() => {
		if (startInEditMode && !isEditing) {
			isEditing = true;
			editValue = pillar;
		}
	});

	function startEdit() {
		isEditing = true;
		editValue = pillar;
	}

	function commitSave() {
		onSave(editValue.trim());
		isEditing = false;
	}

	function cancelEdit() {
		isEditing = false;
	}
</script>

<Item.Root variant="outline" size="sm" class="opacity-100 rounded-3xl">
	{#if isEditing}
		<Item.Content class="flex-1 min-w-0 w-full">
			<Textarea
				bind:value={editValue}
				class="min-h-16 resize-y text-sm"
				placeholder="Pillar description"
				onkeydown={(e: KeyboardEvent) => {
					if (e.key === 'Escape') cancelEdit();
					if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
						e.preventDefault();
						commitSave();
					}
				}}
				onblur={commitSave}
				rows={2}
				autofocus
			/>
		</Item.Content>
	{:else}
		<Item.Content
			class="flex-1 min-w-0 w-full cursor-pointer"
			onclick={() => !readonly && startEdit()}
			onkeydown={(e: KeyboardEvent) => {
				if (!readonly && (e.key === 'Enter' || e.key === ' ')) {
					e.preventDefault();
					startEdit();
				}
			}}
			role={readonly ? undefined : 'button'}
			tabindex={readonly ? undefined : 0}
		>
			<Item.Title class="whitespace-pre-wrap break-words w-full min-w-0 text-left"
				>{pillar || 'Untitled'}</Item.Title
			>
		</Item.Content>
	{/if}
	{#if !readonly && !isEditing}
		<Item.Actions
			class="flex shrink-0 items-center gap-0.5 opacity-0 group-hover/item:opacity-100 transition-opacity duration-150"
		>
			<Button
				type="button"
				variant="ghost"
				size="icon"
				class="cursor-pointer size-8"
				onclick={startEdit}
			>
				<Pencil class="h-4 w-4" />
			</Button>
			<Button
				type="button"
				variant="ghost"
				size="icon"
				class="cursor-pointer size-8 text-destructive hover:text-destructive hover:bg-destructive/10"
				onclick={onRemove}
			>
				<Trash2 class="h-4 w-4" />
			</Button>
		</Item.Actions>
	{/if}
</Item.Root>
