<script lang="ts">
	import BrandSettingsSlider from '$lib/components/brand_settings/BrandSettingsSlider.svelte';
	import { Label } from '$lib/components/ui/label';

	const MIN = 1;
	const MAX = 4;

	interface Props {
		value: number;
		readonly?: boolean;
		class?: string;
	}

	let { value = $bindable(1), readonly = false, class: className }: Props = $props();
</script>

<div class={className}>
	<div class="flex items-center justify-between mb-2">
		<Label class="text-sm font-medium">Industry Jargon</Label>
		<span class="text-xs text-muted-foreground">{value}/{MAX}</span>
	</div>
	<BrandSettingsSlider
		bind:value
		min={MIN}
		max={MAX}
		step={1}
		disabled={readonly}
	/>
</div>
