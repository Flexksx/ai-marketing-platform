<script lang="ts">
	import WordItemToneOfVoiceBrandSetting from '$lib/components/brand_settings/WordItemToneOfVoiceBrandSetting.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import { Plus } from 'lucide-svelte';

	export type ToneWordListVariant = 'must_use' | 'forbidden';

	interface Props {
		title: string;
		words: string[];
		readonly?: boolean;
		variant?: ToneWordListVariant;
		class?: string;
	}

	let {
		title,
		words = $bindable([]),
		readonly = false,
		variant = 'must_use',
		class: className
	}: Props = $props();

	let editingIndex = $state<number | null>(null);

	function addWord() {
		words = [...words, ''];
		editingIndex = words.length - 1;
	}

	function saveWordAt(index: number, newValue: string) {
		if (newValue) {
			words = words.with(index, newValue);
		} else {
			words = words.filter((_, i) => i !== index);
		}
		editingIndex = null;
	}

	function removeWord(index: number) {
		words = words.filter((_, i) => i !== index);
		if (editingIndex === index) editingIndex = null;
		else if (editingIndex !== null && editingIndex > index) editingIndex = editingIndex - 1;
	}

	const hasWords = $derived(words.length > 0);
</script>

<div class={className}>
	<div class="mb-2 flex items-center justify-between">
		<Label class="text-sm font-medium text-muted-foreground">{title}</Label>
		{#if !readonly}
			<Button type="button" variant="ghost" size="sm" onclick={addWord}>
				<Plus class="h-4 w-4 mr-1" />
				Add
			</Button>
		{/if}
	</div>
	{#if hasWords}
		<div class="flex flex-wrap items-center gap-x-1.5 gap-y-1">
			{#each words as word, index (index)}
				<WordItemToneOfVoiceBrandSetting
					{word}
					{readonly}
					startInEditMode={editingIndex === index}
					onSave={(newValue) => saveWordAt(index, newValue)}
					onRemove={() => removeWord(index)}
					{variant}
				/>
			{/each}
		</div>
	{:else if !readonly}
		<p class="text-muted-foreground italic text-sm">None yet. Add one above.</p>
	{:else}
		<p class="text-muted-foreground italic text-sm">None yet.</p>
	{/if}
</div>
