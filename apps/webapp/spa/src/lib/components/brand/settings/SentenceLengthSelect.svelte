<script lang="ts">
	import * as Select from '$lib/components/ui/select';
	import { Label } from '$lib/components/ui/label';

	type SentenceLengthPreference = 'SHORT' | 'MEDIUM' | 'LONG';

	const SENTENCE_LENGTH_OPTIONS: { value: SentenceLengthPreference; label: string }[] = [
		{ value: 'SHORT', label: 'Short' },
		{ value: 'MEDIUM', label: 'Medium' },
		{ value: 'LONG', label: 'Long' }
	];

	interface Props {
		value: SentenceLengthPreference;
		readonly?: boolean;
		class?: string;
	}

	let { value = $bindable('MEDIUM'), readonly = false, class: className }: Props = $props();

	const selectedLabel = $derived(
		SENTENCE_LENGTH_OPTIONS.find((o) => o.value === value)?.label ?? value
	);
</script>

<div class={className}>
	<Label class="text-sm font-medium mb-2 block">Sentence length</Label>
	{#if readonly}
		<p class="text-sm text-muted-foreground py-2">{selectedLabel}</p>
	{:else}
		<Select.Root type="single" bind:value>
			<Select.Trigger class="w-full">
				{selectedLabel}
			</Select.Trigger>
			<Select.Content>
				{#each SENTENCE_LENGTH_OPTIONS as option (option.value)}
					<Select.Item value={option.value} label={option.label}>
						{option.label}
					</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>
	{/if}
</div>
