<script lang="ts">
	import { Building2, Upload } from 'lucide-svelte';

	type Props = {
		logoUrl: string | null | undefined;
		brandName: string;
		pendingFile: File | null;
		onFileSelected: (file: File) => void;
		readonly?: boolean;
	};

	let { logoUrl, brandName, pendingFile, onFileSelected, readonly = false }: Props = $props();

	let fileInput = $state<HTMLInputElement | null>(null);
	let previewUrl = $state<string | null>(null);

	const ACCEPTED_TYPES = 'image/svg+xml,image/png,image/jpeg,image/jpg,image/webp';

	$effect(() => {
		if (pendingFile === null && previewUrl) {
			URL.revokeObjectURL(previewUrl);
			previewUrl = null;
		}
	});

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;

		if (previewUrl) {
			URL.revokeObjectURL(previewUrl);
		}
		previewUrl = URL.createObjectURL(file);
		onFileSelected(file);
		input.value = '';
	}

	function openFilePicker() {
		if (readonly) return;
		fileInput?.click();
	}

	const displayUrl = $derived(previewUrl ?? logoUrl);
</script>

<button
	type="button"
	class="group relative flex-shrink-0 h-20 w-20 rounded-xl overflow-hidden focus:outline-none focus-visible:ring-2 focus-visible:ring-ring {readonly
		? 'cursor-default'
		: 'cursor-pointer'}"
	onclick={openFilePicker}
	disabled={readonly}
	aria-label="Upload brand logo"
>
	{#if displayUrl}
		<div
			class="h-full w-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center shadow-md"
		>
			<img src={displayUrl} alt={brandName} class="h-full w-full object-contain" />
		</div>
	{:else}
		<div class="flex h-full w-full items-center justify-center bg-blue-600 shadow-md">
			<Building2 class="h-10 w-10 text-white" />
		</div>
	{/if}

	{#if !readonly}
		<div
			class="absolute inset-0 flex items-center justify-center bg-black/50 opacity-0 transition-opacity group-hover:opacity-100"
		>
			<Upload class="h-6 w-6 text-white" />
		</div>
	{/if}
</button>

<input
	bind:this={fileInput}
	type="file"
	accept={ACCEPTED_TYPES}
	class="hidden"
	onchange={handleFileChange}
/>
