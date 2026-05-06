<script lang="ts">
	import BrandSettingsSlider from '$lib/components/brand_settings/BrandSettingsSlider.svelte';
	import {
		TONE_DIMENSION_DATA,
		getLevelDescription,
		type ToneDimensionKey
	} from '$lib/components/brand_settings/tone_of_voice_data';
	import { Label } from '$lib/components/ui/label';

	const MIN = 1;
	const MAX = 4;

	interface Props {
		dimensionKey: ToneDimensionKey;
		value: number;
		readonly?: boolean;
		class?: string;
	}

	let { dimensionKey, value = $bindable(1), readonly = false, class: className }: Props = $props();

	const dimension = $derived(TONE_DIMENSION_DATA[dimensionKey]);
	const levelInfo = $derived(getLevelDescription(dimensionKey, value));
</script>

<div class={className}>
	<div class="flex items-center justify-between mb-2">
		<Label class="text-sm font-medium">{dimension.label}</Label>
		<span class="text-xs text-muted-foreground">{levelInfo?.name ?? `${value}/${MAX}`}</span>
	</div>
	<BrandSettingsSlider
		bind:value
		min={MIN}
		max={MAX}
		step={1}
		disabled={readonly}
	/>
	{#if levelInfo}
		<p class="mt-2 text-xs text-muted-foreground">
			{levelInfo.description}
		</p>
	{/if}
</div>
