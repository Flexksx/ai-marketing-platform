<script lang="ts">
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import ColorPicker from 'svelte-awesome-color-picker';

	const DEFAULT_SLIDER_DIRECTION = 'vertical';

	interface Props {
		label: string;
		color: string;
		placeholder: string;
		size?: 'small' | 'medium' | 'large';
	}

	let { label, color = $bindable(), placeholder, size = 'medium' }: Props = $props();

	let boxHeight = $derived(size === 'small' ? 'h-12' : size === 'large' ? 'h-28' : 'h-20');
	let isOpen = $state(false);
	let pickerElement = $state<HTMLDivElement | undefined>(undefined);

	const quickSteps = [12, -12, 25, -25];

	function normalizeHex(value: string) {
		if (!value) return '#000000';
		return value.startsWith('#') ? value : `#${value}`;
	}

	function setColorFromInput(value: string) {
		const hexRegex = /^#?[0-9A-Fa-f]{6}$/;
		if (hexRegex.test(value) || hexRegex.test('#' + value)) {
			color = normalizeHex(value);
		}
	}

	let popoverX = $state(0);
	let popoverY = $state(0);

	function openPicker(event: MouseEvent) {
		isOpen = true;
		const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
		popoverX = rect.left;
		popoverY = rect.bottom + 12;
	}

	function handleClickOutside(event: MouseEvent) {
		if (pickerElement && !pickerElement.contains(event.target as Node)) {
			isOpen = false;
		}
	}

	function hexToRgb(hex: string) {
		const normalized = normalizeHex(hex);
		const bigint = Number.parseInt(normalized.slice(1), 16);
		return {
			r: (bigint >> 16) & 255,
			g: (bigint >> 8) & 255,
			b: bigint & 255
		};
	}

	function rgbToHex(r: number, g: number, b: number) {
		return (
			'#' +
			[r, g, b]
				.map((c) => {
					const v = Math.max(0, Math.min(255, Math.round(c)));
					return v.toString(16).padStart(2, '0');
				})
				.join('')
		);
	}

	function adjustBrightness(hex: string, amount: number) {
		const { r, g, b } = hexToRgb(hex);
		return rgbToHex(r + amount, g + amount, b + amount);
	}

	function getReadableTextColor(hex: string) {
		const { r, g, b } = hexToRgb(hex);
		const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
		return luminance > 0.6 ? '#0f172a' : '#ffffff';
	}

	const variationSwatches = $derived(() =>
		quickSteps.map((step) => ({
			value: adjustBrightness(color, step),
			label: step > 0 ? `+${step}` : `${step}`
		}))
	);

	$effect(() => {
		if (isOpen) {
			document.addEventListener('mousedown', handleClickOutside);
			return () => {
				document.removeEventListener('mousedown', handleClickOutside);
			};
		}
	});
</script>

<div class="space-y-3 rounded-2xl border border-slate-200/60 bg-white/80 p-4 shadow-sm backdrop-blur dark:border-slate-700/60 dark:bg-slate-900/40">
	<div class="flex items-center justify-between">
		<Label class="text-sm font-semibold text-slate-600 dark:text-slate-200">{label}</Label>
		<span class="font-mono text-xs text-slate-500">{color}</span>
	</div>

	<div class="relative">
		<button
			type="button"
			class="{boxHeight} w-full overflow-hidden rounded-xl border border-slate-200 shadow-inner transition-all hover:-translate-y-0.5 hover:shadow-lg dark:border-slate-700"
			style="background: linear-gradient(120deg, {adjustBrightness(color, 20)}, {color});"
			onclick={openPicker}
			aria-label={`Choose ${label.toLowerCase()}`}
		>
			<div
				class="flex h-full w-full items-center justify-between px-4 text-sm font-medium transition-all"
				style={`color: ${getReadableTextColor(color)};`}
			>
				<span>Tap to adjust</span>
				<span class="text-xs opacity-80">Advanced picker</span>
			</div>
		</button>
	</div>

	{#if isOpen}
		<div
			class="fixed left-0 top-0 z-[99999] flex h-screen w-screen items-start justify-start"
			style={`padding-left:${popoverX}px; padding-top:${popoverY}px;`}
		>
			<div
				bind:this={pickerElement}
				class="rounded-2xl border border-slate-200 bg-white p-3 shadow-2xl dark:border-slate-700 dark:bg-slate-900"
			>
				<ColorPicker
					bind:hex={color}
					label=""
					isDialog={false}
					sliderDirection={DEFAULT_SLIDER_DIRECTION}
				/>
			</div>
		</div>
	{/if}

	<div class="grid grid-cols-4 gap-2">
		{#each variationSwatches as swatch}
			<button
				type="button"
				class="rounded-xl border border-white/70 p-2 text-xs font-medium shadow-sm transition hover:-translate-y-0.5 dark:border-white/10"
				onclick={() => (color = swatch.value)}
				style={`background:${swatch.value}; color:${getReadableTextColor(swatch.value)};`}
			>
				{swatch.label}
			</button>
		{/each}
	</div>

	<Input
		value={color}
		oninput={(e) => setColorFromInput(e.currentTarget.value)}
		{placeholder}
		class="font-mono text-sm"
	/>
</div>

