<script lang="ts">
	import { goto } from '$app/navigation';
	import { useBrandGenerationJob } from '$lib/api/brand-generation-jobs/queries';
	import BrandCreationDialogInputs from './BrandCreationDialogInputs.svelte';
	import BrandCreationDialogPolling from './BrandCreationDialogPolling.svelte';
	import BrandCreationDialogResult from './BrandCreationDialogResult.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Building2, Loader2 } from '@lucide/svelte';

	type Props = {
		open?: boolean;
		jobId?: string | null;
	};

	let { open = $bindable(false), jobId = $bindable(null) }: Props = $props();

	const jobQuery = useBrandGenerationJob(() => jobId ?? undefined);

	const job = $derived(jobQuery.data);
	const brandData = $derived(job?.result?.brandData ?? null);
	const scraperResult = $derived(job?.result?.scraperResult ?? null);
	const isLoading = $derived(jobQuery.isLoading);
	const isError = $derived(jobQuery.isError);
	const error = $derived(jobQuery.error);

	const mode = $derived.by(() => {
		if (!jobId) return 'input';
		if (isLoading) return 'loading';
		if (isError || job?.status === 'failed' || job?.status === 'cancelled') return 'error';
		if (job?.status === 'completed' && brandData) return 'form';
		if (scraperResult && job?.status !== 'completed') return 'analyzing';
		return 'extracting';
	});

	function handleClose() {
		open = false;
		jobId = null;
	}

	function handleGenerateAnother() {
		jobId = null;
	}

	function handleSaveComplete() {
		open = false;
		jobId = null;
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Content
		class="flex h-[85vh] max-h-[85vh] w-max min-w-0 max-w-[calc(100vw-2rem)] flex-col overflow-hidden lg:min-w-[42rem]"
	>
		<Dialog.Header class="shrink-0">
			<Dialog.Title class="flex items-center gap-2">
				<Building2 class="h-5 w-5 text-primary" />
				Create New Brand
			</Dialog.Title>
			<Dialog.Description>
				Extract your brand identity from your website. Enter your website URL and we'll analyze
				your brand.
			</Dialog.Description>
		</Dialog.Header>

		<div class="relative flex min-h-0 flex-1 flex-col overflow-hidden py-4 min-w-0">
			{#if mode === 'input'}
				<BrandCreationDialogInputs />
			{:else if mode === 'loading'}
				<div class="flex flex-col items-center justify-center min-h-[60vh]">
					<Loader2 class="w-12 h-12 text-primary animate-spin mb-4" />
					<p class="text-muted-foreground">Loading brand generation job...</p>
				</div>
			{:else if mode === 'extracting' || mode === 'analyzing'}
				<BrandCreationDialogPolling mode={mode === 'analyzing' ? 'analyzing' : 'extracting'} {scraperResult} />
			{:else if mode === 'form'}
				<BrandCreationDialogResult
					{jobId}
					{brandData}
					onClose={handleSaveComplete}
					onGenerateAnother={handleGenerateAnother}
				/>
			{:else if mode === 'error'}
				<div class="flex flex-col gap-4 py-4">
					<div class="text-sm text-destructive bg-destructive/10 p-3 rounded-lg">
						{#if isError}
							{error instanceof Error ? error.message : 'Failed to load brand generation job'}
						{:else if job?.status === 'failed'}
							Brand generation failed. Please try again.
						{:else if job?.status === 'cancelled'}
							Brand generation was cancelled.
						{:else}
							An unknown error occurred
						{/if}
					</div>
					<Button variant="outline" onclick={handleGenerateAnother} class="w-full">
						Try again
					</Button>
				</div>
			{/if}
		</div>
	</Dialog.Content>
</Dialog.Root>
