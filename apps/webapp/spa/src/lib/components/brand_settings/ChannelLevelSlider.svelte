<script lang="ts">
	import BrandSettingsSlider from '$lib/components/brand_settings/BrandSettingsSlider.svelte';

	const MIN = 0;
	const MAX = 5;

	interface Props {
		value: number;
		type: 'hashtag' | 'emoji';
		disabled?: boolean;
		class?: string;
	}

	let {
		value = $bindable(0),
		type: _type,
		disabled = false,
		class: className
	}: Props = $props();
</script>

<BrandSettingsSlider
	bind:value
	min={MIN}
	max={MAX}
	step={1}
	{disabled}
	class={className}
/>
