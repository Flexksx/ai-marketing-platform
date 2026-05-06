<script lang="ts">
	import type { BrandColor, BrandSettingsFormData } from '$lib/api/brands/model/BrandData';
	import { getColor } from '$lib/components/brand_settings/utils';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import {
		DropdownMenu,
		DropdownMenuContent,
		DropdownMenuTrigger
	} from '$lib/components/ui/dropdown-menu';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Palette } from 'lucide-svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
		variant?: 'card' | 'inline';
	}

	let { data = $bindable(), readonly = false, variant = 'card' }: Props = $props();

	let lastEditSource = $state<Array<'hex' | 'name' | null>>([]);

	// We store the HSV state separately so we don't lose the Hue
	// when dragging into pure black or pure white areas.
	let activeHsv = $state<Record<number, { h: number; s: number; v: number }>>({});

	// --- Color Math Utilities ---
	function hexToHsv(hex: string) {
		let r = 0,
			g = 0,
			b = 0;
		hex = hex.replace(/^#/, '');
		if (hex.length === 3) {
			r = parseInt(hex[0] + hex[0], 16);
			g = parseInt(hex[1] + hex[1], 16);
			b = parseInt(hex[2] + hex[2], 16);
		} else if (hex.length === 6) {
			r = parseInt(hex.slice(0, 2), 16);
			g = parseInt(hex.slice(2, 4), 16);
			b = parseInt(hex.slice(4, 6), 16);
		}
		r /= 255;
		g /= 255;
		b /= 255;

		const max = Math.max(r, g, b),
			min = Math.min(r, g, b);
		const d = max - min;
		let h = 0;
		const s = max === 0 ? 0 : d / max;
		const v = max;

		if (max !== min) {
			switch (max) {
				case r:
					h = (g - b) / d + (g < b ? 6 : 0);
					break;
				case g:
					h = (b - r) / d + 2;
					break;
				case b:
					h = (r - g) / d + 4;
					break;
			}
			h /= 6;
		}
		return { h: h * 360, s: s * 100, v: v * 100 };
	}

	function hsvToHex(h: number, s: number, v: number) {
		h /= 360;
		s /= 100;
		v /= 100;
		let r = 0,
			g = 0,
			b = 0;
		const i = Math.floor(h * 6);
		const f = h * 6 - i;
		const p = v * (1 - s);
		const q = v * (1 - f * s);
		const t = v * (1 - (1 - f) * s);

		switch (i % 6) {
			case 0:
				r = v;
				g = t;
				b = p;
				break;
			case 1:
				r = q;
				g = v;
				b = p;
				break;
			case 2:
				r = p;
				g = v;
				b = t;
				break;
			case 3:
				r = p;
				g = q;
				b = v;
				break;
			case 4:
				r = t;
				g = p;
				b = v;
				break;
			case 5:
				r = v;
				g = p;
				b = q;
				break;
		}

		const toHex = (x: number) => {
			const hexStr = Math.round(x * 255).toString(16);
			return hexStr.length === 1 ? '0' + hexStr : hexStr;
		};
		return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
	}

	// --- Component Logic ---
	function addColor() {
		const defaultColor: BrandColor = {
			name: '#3B82F6',
			hex_value: '#3B82F6'
		};
		data.colors = [...data.colors, defaultColor];
		const index = data.colors.length - 1;
		lastEditSource[index] = 'hex';
		activeHsv[index] = hexToHsv(defaultColor.hex_value);
	}

	function removeColor(index: number) {
		if (index < 0 || index >= data.colors.length) return;
		data.colors = [...data.colors.slice(0, index), ...data.colors.slice(index + 1)];
		delete activeHsv[index];
		lastEditSource = lastEditSource.filter((_, i) => i !== index);
	}
	function updateColorAtIndex(index: number, updates: { hex_value?: string; name?: string }) {
		const color = data.colors[index];
		if (!color) return;

		const updated = { ...color, ...updates };
		data.colors = [...data.colors.slice(0, index), updated, ...data.colors.slice(index + 1)];
	}

	function normalizeHex(value: string | null) {
		if (!value) return '';
		const trimmed = value.trim();
		if (trimmed.startsWith('#')) return trimmed;
		return `#${trimmed}`;
	}

	function handleHexChange(index: number, rawValue: string | null, updateHsvState = true) {
		const hexValue = normalizeHex(rawValue);
		if (!hexValue) return;

		const color = data.colors[index];
		if (!color) return;

		// Sync local HSV state if typed manually in the input
		if (updateHsvState) {
			activeHsv[index] = hexToHsv(hexValue);
		}

		const previousEdit = lastEditSource[index] ?? null;
		lastEditSource[index] = 'hex';

		let name = color.name;
		if (previousEdit !== 'name') {
			name = hexValue;
		}

		updateColorAtIndex(index, { hex_value: hexValue, name });
	}

	function handleNameChange(index: number, value: string) {
		const color = data.colors[index];
		if (!color) return;

		lastEditSource[index] = 'name';
		updateColorAtIndex(index, { name: value });
	}

	function syncInitialHsv(index: number, hex: string) {
		if (!activeHsv[index]) {
			activeHsv[index] = hexToHsv(hex || '#000000');
		}
	}

	// Handles the dragging logic for both the SV square and Hue slider
	function handlePointerDown(e: PointerEvent, index: number, type: 'sv' | 'hue') {
		const target = e.currentTarget as HTMLElement;
		const rect = target.getBoundingClientRect();

		syncInitialHsv(index, data.colors[index]?.hex_value || '#000000');

		function update(clientX: number, clientY: number) {
			const x = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
			const y = Math.max(0, Math.min(1, (clientY - rect.top) / rect.height));

			const current = activeHsv[index];

			if (type === 'sv') {
				activeHsv[index] = { ...current, s: x * 100, v: (1 - y) * 100 };
			} else {
				activeHsv[index] = { ...current, h: x * 360 };
			}

			const newHex = hsvToHex(activeHsv[index].h, activeHsv[index].s, activeHsv[index].v);
			handleHexChange(index, newHex, false); // false = don't overwrite our active drag state
		}

		update(e.clientX, e.clientY);

		function onPointerMove(moveEvent: PointerEvent) {
			update(moveEvent.clientX, moveEvent.clientY);
		}

		function onPointerUp() {
			window.removeEventListener('pointermove', onPointerMove);
			window.removeEventListener('pointerup', onPointerUp);
		}

		window.addEventListener('pointermove', onPointerMove);
		window.addEventListener('pointerup', onPointerUp);
	}
</script>

{#if variant === 'card'}
	<Card
		class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80 h-full flex flex-col"
	>
		<CardHeader>
			<CardTitle class="flex items-center gap-2">
				<Palette class="h-5 w-5" />
				Brand Colors
			</CardTitle>
		</CardHeader>
		<CardContent class="flex-1 flex flex-col items-center justify-center gap-4">
			{#if data.colors.length > 0}
				{#if readonly}
					<div class="flex items-center justify-center gap-3 w-full flex-wrap">
						{#each data.colors as color (color.name)}
							<div class="group flex flex-col items-center gap-1.5">
								<div
									class="relative h-14 w-14 rounded-full border-2 border-white shadow-md dark:border-slate-700"
									style="background-color: {getColor(color.hex_value, '#3B82F6')};"
								></div>
								<span
									class="text-xs font-medium text-slate-600 dark:text-slate-400 text-center w-[72px] truncate"
								>
									{color.name}
								</span>
							</div>
						{/each}
					</div>
				{:else}
					<div class="flex items-center justify-center gap-3 w-full flex-wrap">
						{#each data.colors as color, index (index)}
							<div class="group flex flex-col items-center gap-1.5">
								<DropdownMenu
									onOpenChange={(open) => {
										if (open) syncInitialHsv(index, color.hex_value || '#000000');
									}}
								>
									<DropdownMenuTrigger
										class="relative mt-1 h-10 w-10 rounded-full border-2 border-white shadow-md dark:border-slate-700 cursor-pointer hover:scale-110 transition-transform"
										style="background-color: {getColor(color.hex_value, '#3B82F6')};"
										aria-label={`Edit ${color.name} color`}
									/>
									<DropdownMenuContent align="center" class="w-72 space-y-4 p-4">
										<div class="flex items-center gap-3">
											<div
												class="h-6 w-6 rounded-full border border-border shadow-inner"
												style="background-color: {getColor(color.hex_value, '#3B82F6')};"
											></div>
											<span class="text-sm font-semibold text-slate-800 dark:text-slate-100 truncate">
												{color.name}
											</span>
										</div>

										<div class="space-y-3">
											<div
												class="relative h-36 w-full cursor-crosshair rounded-md overflow-hidden shadow-sm"
												style="background-color: hsl({activeHsv[index]?.h || 0}, 100%, 50%);"
												onpointerdown={(e) => handlePointerDown(e, index, 'sv')}
												role="slider"
												tabindex="0"
												aria-label="Saturation and brightness"
												aria-valuenow={Math.round(activeHsv[index]?.s || 0)}
												aria-valuemin="0"
												aria-valuemax="100"
											>
												<div
													class="absolute inset-0 bg-gradient-to-r from-white to-transparent"
												></div>
												<div
													class="absolute inset-0 bg-gradient-to-t from-black to-transparent"
												></div>
												<div
													class="absolute h-4 w-4 -translate-x-2 -translate-y-2 rounded-full border-2 border-white shadow-md pointer-events-none"
													style="left: {activeHsv[index]?.s || 0}%; top: {100 -
														(activeHsv[index]?.v || 0)}%;"
												></div>
											</div>

											<div
												class="relative h-4 w-full cursor-pointer rounded-full shadow-sm"
												style="background: linear-gradient(to right, #f00 0%, #ff0 17%, #0f0 33%, #0ff 50%, #00f 67%, #f0f 83%, #f00 100%);"
												onpointerdown={(e) => handlePointerDown(e, index, 'hue')}
												role="slider"
												tabindex="0"
												aria-label="Hue"
												aria-valuenow={Math.round(activeHsv[index]?.h || 0)}
												aria-valuemin="0"
												aria-valuemax="360"
											>
												<div
													class="absolute top-1/2 h-5 w-5 -translate-x-2.5 -translate-y-1/2 rounded-full border-2 border-white bg-white shadow-md pointer-events-none"
													style="left: {(activeHsv[index]?.h || 0) / 3.6}%;"
												></div>
											</div>
										</div>

										<div class="grid grid-cols-2 gap-3 pt-1">
											<div class="space-y-1.5">
												<Label class="text-xs font-medium text-muted-foreground">Name</Label>
												<Input
													class="h-8 text-sm"
													value={color.name}
													oninput={(event) =>
														handleNameChange(
															index,
															(event.currentTarget as HTMLInputElement).value
														)}
												/>
											</div>
											<div class="space-y-1.5">
												<Label class="text-xs font-medium text-muted-foreground">Hex</Label>
												<Input
													class="h-8 text-sm uppercase"
													type="text"
													value={color.hex_value || ''}
													placeholder="#000000"
													oninput={(event) =>
														handleHexChange(
															index,
															(event.currentTarget as HTMLInputElement).value
														)}
												/>
											</div>
										</div>
										<button
											type="button"
											class="mt-2 inline-flex items-center gap-1 rounded-full border border-destructive/40 px-2 py-1 text-[11px] font-medium text-destructive hover:bg-destructive/10"
											onclick={() => removeColor(index)}
										>
											<span class="text-xs leading-none">×</span>
											Remove color
										</button>
									</DropdownMenuContent>
								</DropdownMenu>
								<span
									class="text-xs font-medium text-slate-600 dark:text-slate-400 text-center w-[72px] truncate"
								>
									{color.name}
								</span>
							</div>
						{/each}
					</div>
				{/if}
			{:else}
				<p class="text-muted-foreground italic text-sm">No colors yet...</p>
			{/if}

			{#if !readonly}
				<button
					type="button"
					class="mt-2 inline-flex items-center gap-2 rounded-full border border-dashed border-slate-300 px-3 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800"
					onclick={addColor}
				>
					<span class="text-base leading-none">+</span>
					Add color
				</button>
			{/if}
		</CardContent>
	</Card>
{:else}
	<div class="flex flex-wrap items-center gap-2">
		{#if data.colors.length > 0}
			{#if readonly}
				{#each data.colors as color (color.name)}
					<div class="flex w-16 flex-col items-center gap-1.5 px-1">
						<div
							class="h-10 w-10 rounded-full border-2 border-white shadow-md dark:border-slate-700"
							style="background-color: {getColor(color.hex_value, '#3B82F6')};"
						></div>
						<span
							class="w-full truncate text-center text-[11px] font-medium text-slate-600 dark:text-slate-400"
						>
							{color.name}
						</span>
					</div>
				{/each}
			{:else}
				{#each data.colors as color, index (index)}
					<div class="group flex w-16 flex-col items-center gap-1.5 px-1">
						<DropdownMenu
							onOpenChange={(open) => {
								if (open) syncInitialHsv(index, color.hex_value || '#000000');
							}}
						>
							<DropdownMenuTrigger
								class="relative h-10 w-10 rounded-full border-2 border-white shadow-md dark:border-slate-700 cursor-pointer hover:scale-110 transition-transform"
								style="background-color: {getColor(color.hex_value, '#3B82F6')};"
								aria-label={`Edit ${color.name} color`}
							/>
							<DropdownMenuContent align="center" class="w-72 space-y-4 p-4">
								<div class="flex items-center gap-">
									<div
										class="h-6 w-6 rounded-full border border-border shadow-inner"
										style="background-color: {getColor(color.hex_value, '#3B82F6')};"
									></div>
									<span class="text-sm font-semibold text-slate-800 dark:text-slate-100 truncate">
										{color.name}
									</span>
								</div>

								<div class="space-y-3">
									<div
										class="relative h-36 w-full cursor-crosshair rounded-md overflow-hidden shadow-sm"
										style="background-color: hsl({activeHsv[index]?.h || 0}, 100%, 50%);"
										onpointerdown={(e) => handlePointerDown(e, index, 'sv')}
										role="slider"
										tabindex="0"
										aria-label="Saturation and brightness"
										aria-valuenow={Math.round(activeHsv[index]?.s || 0)}
										aria-valuemin="0"
										aria-valuemax="100"
									>
										<div
											class="absolute inset-0 bg-gradient-to-r from-white to-transparent"
										></div>
										<div
											class="absolute inset-0 bg-gradient-to-t from-black to-transparent"
										></div>
										<div
											class="absolute h-4 w-4 -translate-x-2 -translate-y-2 rounded-full border-2 border-white shadow-md pointer-events-none"
											style="left: {activeHsv[index]?.s || 0}%; top: {100 -
												(activeHsv[index]?.v || 0)}%;"
										></div>
									</div>

									<div
										class="relative h-4 w-full cursor-pointer rounded-full shadow-sm"
										style="background: linear-gradient(to right, #f00 0%, #ff0 17%, #0f0 33%, #0ff 50%, #00f 67%, #f0f 83%, #f00 100%);"
										onpointerdown={(e) => handlePointerDown(e, index, 'hue')}
										role="slider"
										tabindex="0"
										aria-label="Hue"
										aria-valuenow={Math.round(activeHsv[index]?.h || 0)}
										aria-valuemin="0"
										aria-valuemax="360"
									>
										<div
											class="absolute top-1/2 h-5 w-5 -translate-x-2.5 -translate-y-1/2 rounded-full border-2 border-white bg-white shadow-md pointer-events-none"
											style="left: {(activeHsv[index]?.h || 0) / 3.6}%;"
										></div>
									</div>
								</div>

								<div class="grid grid-cols-2 gap-3 pt-1">
									<div class="space-y-1.5">
										<Label class="text-xs font-medium text-muted-foreground">Name</Label>
										<Input
											class="h-8 text-sm"
											value={color.name}
											oninput={(event) =>
												handleNameChange(
													index,
													(event.currentTarget as HTMLInputElement).value
												)}
										/>
									</div>
									<div class="space-y-1.5">
										<Label class="text-xs font-medium text-muted-foreground">Hex</Label>
										<Input
											class="h-8 text-sm uppercase"
											type="text"
											value={color.hex_value || ''}
											placeholder="#000000"
											oninput={(event) =>
												handleHexChange(
													index,
													(event.currentTarget as HTMLInputElement).value
												)}
										/>
									</div>
								</div>
								<button
									type="button"
									class="mt-2 inline-flex items-center gap-1 rounded-full border border-destructive/40 px-2 py-1 text-[11px] font-medium text-destructive hover:bg-destructive/10"
									onclick={() => removeColor(index)}
								>
									<span class="text-xs leading-none">×</span>
									Remove color
								</button>
							</DropdownMenuContent>
						</DropdownMenu>
						<span
							class="w-full truncate text-center text-[11px] font-medium text-slate-600 dark:text-slate-400"
						>
							{color.name}
						</span>
					</div>
				{/each}

				<button
					type="button"
					class="inline-flex items-center gap-2 rounded-full border border-dashed border-slate-300 px-3 py-1 text-[11px] font-medium text-slate-600 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800"
					onclick={addColor}
				>
					<span class="text-base leading-none">+</span>
					Add color
				</button>
			{/if}
		{:else}
			{#if readonly}
				<p class="text-xs text-muted-foreground italic">No colors yet...</p>
			{:else}
				<button
					type="button"
					class="inline-flex items-center gap-2 rounded-full border border-dashed border-slate-300 px-3 py-1 text-[11px] font-medium text-slate-600 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800"
					onclick={addColor}
				>
					<span class="text-base leading-none">+</span>
					Add first color
				</button>
			{/if}
		{/if}
	</div>
{/if}
