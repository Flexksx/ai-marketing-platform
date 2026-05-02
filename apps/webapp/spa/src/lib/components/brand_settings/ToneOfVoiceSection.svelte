<script lang="ts">
	import { defaultToneOfVoice, type BrandSettingsFormData } from './form-data';
	import ToneDimensionSlider from '$lib/components/brand_settings/ToneDimensionSlider.svelte';
	import ToneWordList from '$lib/components/brand_settings/ToneWordList.svelte';
	import { Card, CardContent } from '$lib/components/ui/card';
	import * as Select from '$lib/components/ui/select';
	import { BRAND_ARCHETYPE_NAMES, getArchetypeDescription, getArchetypeLabel } from '$lib/utils/brandArchetype';
	import type { BrandArchetypeName } from '$lib/api/generated/models/BrandArchetypeName';
	import { Mic2 } from 'lucide-svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
	}

	let { data = $bindable(), readonly = false }: Props = $props();

	const NONE_VALUE = '';

	let selectedArchetype = $state('');

	$effect(() => {
		selectedArchetype = data.toneOfVoice?.archetype ?? NONE_VALUE;
	});
	$effect(() => {
		if (!readonly && data.toneOfVoice) {
			data.toneOfVoice = {
				...data.toneOfVoice,
				archetype: selectedArchetype === NONE_VALUE ? null : (selectedArchetype as BrandArchetypeName)
			};
		}
	});

	const archetypeTriggerLabel = $derived(
		selectedArchetype === NONE_VALUE
			? 'Select archetype'
			: getArchetypeLabel(selectedArchetype as BrandArchetypeName)
	);

	const archetypeDescription = $derived(
		selectedArchetype !== NONE_VALUE
			? getArchetypeDescription(selectedArchetype as BrandArchetypeName)
			: null
	);

	function ensureToneOfVoice() {
		if (!data.toneOfVoice) {
			data.toneOfVoice = { ...defaultToneOfVoice };
		}
	}

	$effect(() => {
		if (!readonly) ensureToneOfVoice();
	});
</script>

<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80 h-full">
	<CardContent class="p-6">
		<div class="mb-4 flex items-center justify-between">
			<h3 class="text-lg font-semibold flex items-center gap-2">
				<Mic2 class="h-5 w-5 text-violet-600" />
				Brand Voice
			</h3>
		</div>
		{#if data.toneOfVoice}
			<div class="space-y-6">
				<div>
					<p class="text-sm text-muted-foreground mb-2">Archetype</p>
					{#if readonly}
						{#if data.toneOfVoice.archetype}
							<span class="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
								{getArchetypeLabel(data.toneOfVoice.archetype as BrandArchetypeName)}
							</span>
							{#if archetypeDescription}
								<p class="mt-2 text-sm text-muted-foreground italic">{archetypeDescription}</p>
							{/if}
						{:else}
							<p class="text-muted-foreground italic text-sm">No archetype selected...</p>
						{/if}
					{:else}
						<Select.Root type="single" bind:value={selectedArchetype}>
							<Select.Trigger class="w-full h-10">
								{archetypeTriggerLabel}
							</Select.Trigger>
							<Select.Content class="max-h-[300px]">
								<Select.Item value={NONE_VALUE} label="None">None</Select.Item>
								{#each BRAND_ARCHETYPE_NAMES as name (name)}
									<Select.Item value={name} label={getArchetypeLabel(name)}>
										{getArchetypeLabel(name)}
									</Select.Item>
								{/each}
							</Select.Content>
						</Select.Root>
						{#if archetypeDescription}
							<p class="mt-2 text-sm text-muted-foreground italic">{archetypeDescription}</p>
						{/if}
					{/if}
				</div>

				<div class="space-y-4">
					<ToneDimensionSlider
						dimensionKey="jargon_density"
						bind:value={data.toneOfVoice.jargonDensity!}
						{readonly}
					/>
					<ToneDimensionSlider
						dimensionKey="visual_density"
						bind:value={data.toneOfVoice.visualDensity!}
						{readonly}
					/>
				</div>

				<ToneWordList
					title="Must-Use Words"
					bind:words={data.toneOfVoice.mustUseWords!}
					variant="must_use"
					{readonly}
				/>
				<ToneWordList
					title="Forbidden Words"
					bind:words={data.toneOfVoice.forbiddenWords!}
					variant="forbidden"
					{readonly}
				/>
			</div>
		{:else}
			<p class="text-muted-foreground italic">No brand voice data yet...</p>
		{/if}
	</CardContent>
</Card>
