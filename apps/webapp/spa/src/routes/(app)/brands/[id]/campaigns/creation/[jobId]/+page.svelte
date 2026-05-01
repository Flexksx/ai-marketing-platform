<script lang="ts">
	import { page } from '$app/state';
	import { navigate } from '$lib/navigation';
	import { useCampaignGenerationJob } from '$lib/api/campaign-generation-jobs';
	import CampaignCreationPhases from '$lib/components/campaign/CampaignCreationPhases.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Loader2 } from 'lucide-svelte';
	import { fade } from 'svelte/transition';

	const jobId = $derived(page.params.jobId);
	const brandId = $derived(page.params.id);

	const jobQuery = useCampaignGenerationJob(
		() => brandId,
		() => jobId
	);
	const job = $derived(jobQuery.data);
	const isLoading = $derived(jobQuery.isLoading);
	const isError = $derived(jobQuery.isError);
	const error = $derived(jobQuery.error);

	const brandData = $derived.by(() => {
		const layoutData = page.data as {
			brand?: { name: string; logoUrl: string | null; mediaUrls?: string[] };
		};
		return {
			name: layoutData.brand?.name ?? '',
			logoUrl: layoutData.brand?.logoUrl || null,
			mediaUrls: layoutData.brand?.mediaUrls || []
		};
	});
</script>

{#if isLoading}
	<div class="w-full h-screen flex items-center justify-center" in:fade={{ duration: 300 }}>
		<Card class="max-w-md">
			<CardContent class="p-8 text-center">
				<Loader2 class="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
				<h3 class="text-xl font-semibold mb-2">Loading Content Plan</h3>
				<p class="text-muted-foreground">
					Please wait while we fetch your content plan details...
				</p>
			</CardContent>
		</Card>
	</div>
{:else if isError}
	<div class="w-full h-screen flex items-center justify-center" in:fade={{ duration: 300 }}>
		<Card class="max-w-md border-destructive">
			<CardContent class="p-8 text-center">
				<div class="text-destructive text-4xl mb-4">⚠️</div>
				<h3 class="text-xl font-semibold mb-2">Failed to Load Content Plan</h3>
				<p class="text-muted-foreground mb-4">
					{error instanceof Error ? error.message : 'An unknown error occurred'}
				</p>
				<Button variant="outline" onclick={() => navigate(`/brands/${brandId}`)}>Back to Brand</Button>
			</CardContent>
		</Card>
	</div>
{:else if job}
	<div class="w-full" in:fade={{ duration: 400 }}>
		<CampaignCreationPhases
			result={job.result}
			brandName={brandData.name}
			brandLogoUrl={brandData.logoUrl}
			jobStatus={job.status}
			{jobId}
			{brandId}
		/>
	</div>
{/if}
