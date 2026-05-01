<script lang="ts">
	import { Slider } from '$lib/components/ui/slider';

	interface Props {
		value: number;
		min: number;
		max: number;
		step?: number;
		disabled?: boolean;
		class?: string;
		rangeColor?: string;
	}

	let {
		value = $bindable(0),
		min,
		max,
		step = 1,
		disabled = false,
		class: className,
		rangeColor
	}: Props = $props();
</script>

{#if rangeColor}
	<div style="--slider-range-color: {rangeColor}" class={className}>
		<Slider
			type="single"
			bind:value
			{min}
			{max}
			{step}
			{disabled}
			class="[&_[data-slot=slider-range]]:!bg-[var(--slider-range-color)]"
		/>
	</div>
{:else}
	<Slider
		type="single"
		bind:value
		{min}
		{max}
		{step}
		{disabled}
		class={className}
	/>
{/if}
