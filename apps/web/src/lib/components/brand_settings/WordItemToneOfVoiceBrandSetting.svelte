<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import * as Item from '$lib/components/ui/item';
	import { cn } from '$lib/utils';
	import { tick } from 'svelte';
	import { X } from 'lucide-svelte';

	export type WordItemToneOfVoiceVariant = 'sensory' | 'excluded' | 'signature';

	interface Props {
		word: string;
		readonly?: boolean;
		startInEditMode?: boolean;
		onSave: (newValue: string) => void;
		onRemove: () => void;
		variant: WordItemToneOfVoiceVariant;
	}

	let { word, readonly = false, startInEditMode = false, onSave, onRemove, variant }: Props =
		$props();
	let isEditing = $state(false);
	let editValue = $state('');
	let mirrorRef = $state<HTMLSpanElement | null>(null);
	let inputWidth = $state(48);

	$effect(() => {
		if (startInEditMode && !isEditing) {
			isEditing = true;
			editValue = word;
		}
	});

	$effect(() => {
		if (!isEditing || !mirrorRef || editValue === undefined) return;
		mirrorRef.textContent = editValue || '\u00A0';
		tick().then(() => {
			if (!mirrorRef) return;
			const w = mirrorRef.getBoundingClientRect().width;
			inputWidth = Math.max(48, Math.ceil(w) + 8);
		});
	});

	function startEdit() {
		isEditing = true;
		editValue = word;
	}

	function commitSave() {
		const trimmed = editValue.trim();
		onSave(trimmed);
		isEditing = false;
	}

	function cancelEdit() {
		isEditing = false;
	}

	const variantClass = $derived(
		variant === 'sensory'
			? 'border-blue-200 bg-blue-100/80 dark:border-blue-800 dark:bg-blue-900/25 text-foreground'
			: variant === 'excluded'
				? 'border-red-200 bg-red-100/80 dark:border-red-800 dark:bg-red-900/25 text-foreground'
				: 'border-primary/40 bg-primary/10 text-foreground'
	);
</script>

<Item.Root
	variant="outline"
	size="sm"
	class={cn(
		'!gap-1 !px-2 !py-0.5 opacity-100 w-fit rounded-full text-xs font-medium inline-flex',
		variantClass
	)}
>
	{#if isEditing}
		<Item.Content class="relative min-w-0 flex-1">
			<span
				bind:this={mirrorRef}
				class="pointer-events-none invisible absolute left-0 top-0 whitespace-pre text-xs font-medium"
				aria-hidden="true"
			></span>
			<Input
				type="text"
				class="h-5 min-w-0 border-0 bg-transparent p-0 text-xs shadow-none focus-visible:ring-0"
				style="width: {inputWidth}px"
				placeholder="Word or phrase"
				value={editValue}
				oninput={(e: Event) => (editValue = (e.currentTarget as HTMLInputElement).value)}
				onkeydown={(e: KeyboardEvent) => {
					if (e.key === 'Enter') commitSave();
					if (e.key === 'Escape') cancelEdit();
				}}
				onblur={commitSave}
				autofocus
			/>
		</Item.Content>
	{:else}
		<Item.Content
			class="flex-1 min-w-0 cursor-pointer"
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
			<Item.Title>{word || 'Untitled'}</Item.Title>
		</Item.Content>
	{/if}
	{#if !readonly && !isEditing}
		<Item.Actions
			class="flex shrink-0 items-center opacity-0 group-hover/item:opacity-100 transition-opacity duration-150"
		>
			<Button
				type="button"
				variant="ghost"
				size="icon"
				class="cursor-pointer size-5 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
				onclick={onRemove}
			>
				<X class="h-3 w-3" />
			</Button>
		</Item.Actions>
	{/if}
</Item.Root>
