<script lang="ts">
	import { page } from '$app/state';
	import { navigate } from '$lib/navigation';
	import { useBrandGenerationJob } from '$lib/resources/brand-generation-jobs/queries';
	import { BrandGenerationJobPolling, BrandGenerationJobResult } from '$lib/components/brand_generation_job';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Building2, Loader2 } from '@lucide/svelte';

	const jobId = $derived(page.params.jobId);

	const jobQuery = useBrandGenerationJob(() => jobId ?? undefined);

	const job = $derived(jobQuery.data);
	const brandData = $derived(job?.result?.brandData ?? null);
	const scraperResult = $derived(job?.result?.scraperResult ?? null);
	const isLoading = $derived(jobQuery.isLoading);
	const isError = $derived(jobQuery.isError);
	const error = $derived(jobQuery.error);

	const mode = $derived.by(() => {
		if (isLoading) return 'loading';
		if (isError || job?.status === 'failed' || job?.status === 'cancelled') return 'error';
		if (job?.status === 'completed' && brandData) return 'form';
		if (scraperResult && job?.status !== 'completed') return 'analyzing';
		return 'extracting';
	});

	function handleGenerateAnother() {
		navigate('/brands/create');
	}

	function handleSaveComplete() {}
</script>

<div class="min-h-screen bg-slate-50 dark:bg-slate-900">
	<div class="container mx-auto px-4 py-8">
		{#if mode === 'loading'}
			<div class="flex flex-col items-center justify-center min-h-[60vh]">
				<Card class="max-w-md">
					<CardContent class="p-8 text-center">
						<Loader2 class="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
						<h3 class="text-xl font-semibold mb-2">Loading Brand Generation</h3>
						<p class="text-muted-foreground">
							Please wait while we fetch your brand generation job...
						</p>
					</CardContent>
				</Card>
			</div>
		{:else if mode === 'error'}
			<div class="flex flex-col items-center justify-center min-h-[60vh]">
				<Card class="max-w-md border-destructive">
					<CardContent class="p-8 text-center">
						<div class="text-destructive text-4xl mb-4">⚠️</div>
						<h3 class="text-xl font-semibold mb-2">Failed to Generate Brand</h3>
						<p class="text-muted-foreground mb-4">
							{#if isError}
								{error instanceof Error ? error.message : 'Failed to load brand generation job'}
							{:else if job?.status === 'failed'}
								Brand generation failed. Please try again.
							{:else if job?.status === 'cancelled'}
								Brand generation was cancelled.
							{:else}
								An unknown error occurred
							{/if}
						</p>
						<Button variant="outline" onclick={handleGenerateAnother}>Try Again</Button>
					</CardContent>
				</Card>
			</div>
		{:else if mode === 'extracting' || mode === 'analyzing'}
			<BrandGenerationJobPolling mode={mode === 'analyzing' ? 'analyzing' : 'extracting'} {scraperResult} />
		{:else if mode === 'form'}
			<div class="max-w-[1800px] mx-auto">
				<BrandGenerationJobResult
					{jobId}
					{brandData}
					onClose={handleSaveComplete}
					onGenerateAnother={handleGenerateAnother}
				/>
			</div>
		{/if}
	</div>
</div>
