<script lang="ts">
	import { ImageIcon, Upload, X } from '@lucide/svelte';

	type Props = {
		file: File | null;
		accept?: string;
		disabled?: boolean;
		onFileChange: (file: File) => void;
		onFileRemove: () => void;
	};

	let {
		file = $bindable(),
		accept = 'image/*',
		disabled = false,
		onFileChange,
		onFileRemove
	}: Props = $props();

	let isDragging = $state(false);
	let fileInputRef = $state<HTMLInputElement | null>(null);

	const handleDragEnter = (e: DragEvent) => {
		if (disabled) return;
		e.preventDefault();
		e.stopPropagation();
		isDragging = true;
	};

	const handleDragLeave = (e: DragEvent) => {
		if (disabled) return;
		e.preventDefault();
		e.stopPropagation();
		if (e.currentTarget === e.target) {
			isDragging = false;
		}
	};

	const handleDragOver = (e: DragEvent) => {
		if (disabled) return;
		e.preventDefault();
		e.stopPropagation();
	};

	const handleDrop = (e: DragEvent) => {
		if (disabled) return;
		e.preventDefault();
		e.stopPropagation();
		isDragging = false;

		const files = e.dataTransfer?.files;
		if (files && files.length > 0) {
			onFileChange(files[0]);
		}
	};

	const handleFileInputChange = (e: Event) => {
		const target = e.target as HTMLInputElement;
		if (target.files && target.files[0]) {
			onFileChange(target.files[0]);
		}
	};

	const handleClick = () => {
		if (disabled || !fileInputRef) return;
		fileInputRef.click();
	};

	const handleRemove = () => {
		if (disabled) return;
		onFileRemove();
		if (fileInputRef) {
			fileInputRef.value = '';
		}
	};

	const previewUrl = $derived(file ? URL.createObjectURL(file) : null);
</script>

<div class="relative">
	<input
		bind:this={fileInputRef}
		type="file"
		{accept}
		{disabled}
		onchange={handleFileInputChange}
		class="hidden"
	/>

	{#if file && previewUrl}
		<div class="relative group">
			<div
				class="relative aspect-video w-full overflow-hidden rounded-lg border-2 border-slate-200"
			>
				<img src={previewUrl} alt={file.name} class="w-full h-full object-cover" />
			</div>
			<button
				type="button"
				onclick={handleRemove}
				{disabled}
				class="absolute -top-2 -right-2 bg-destructive text-destructive-foreground rounded-full p-1.5 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
				aria-label="Remove image"
			>
				<X class="h-4 w-4" />
			</button>
			<p class="text-xs text-muted-foreground mt-2 text-center truncate">{file.name}</p>
		</div>
	{:else}
		<button
			type="button"
			onclick={handleClick}
			ondragenter={handleDragEnter}
			ondragleave={handleDragLeave}
			ondragover={handleDragOver}
			ondrop={handleDrop}
			{disabled}
			class="relative w-full aspect-video rounded-lg border-2 border-dashed transition-colors flex flex-col items-center justify-center gap-3 hover:border-primary hover:bg-primary/5 disabled:opacity-50 disabled:cursor-not-allowed {isDragging
				? 'border-primary bg-primary/10'
				: 'border-slate-300 bg-slate-50'}"
		>
			<div
				class="flex items-center justify-center w-12 h-12 rounded-full transition-colors {isDragging
					? 'bg-primary/20'
					: 'bg-slate-200'}"
			>
				{#if isDragging}
					<Upload class="h-6 w-6 text-primary" />
				{:else}
					<ImageIcon class="h-6 w-6 text-slate-500" />
				{/if}
			</div>
			<div class="text-center">
				<p class="text-sm font-medium text-slate-700">
					{isDragging ? 'Drop image here' : 'Click to upload or drag and drop'}
				</p>
				<p class="text-xs text-muted-foreground mt-1">PNG, JPG, GIF up to 10MB</p>
			</div>
		</button>
	{/if}
</div>
