<script lang="ts">
	import { fly } from 'svelte/transition';
	import { Loader2 } from 'lucide-svelte';
	import { Card, CardContent } from '$lib/components/ui/card';
	import CampaignCreationCalendar from './CampaignCreationCalendar.svelte';
	import type { CampaignContentPlanItem } from '$lib/api/campaign-generation-jobs';

	type Props = {
		contentPlanItems: CampaignContentPlanItem[] | null;
		brandName: string;
		isJobActive?: boolean;
		brandId?: string;
		jobId?: string;
	};

	let { contentPlanItems, brandName, isJobActive = false, brandId, jobId }: Props = $props();

	const hasItems = $derived(!!(contentPlanItems && contentPlanItems.length > 0));

	const totalPosts = $derived(contentPlanItems?.length ?? 0);
	const completedPosts = $derived(
		contentPlanItems?.filter((item) => item.generationStatus === 'completed').length ?? 0
	);
	const loadingPosts = $derived(
		contentPlanItems?.filter(
			(item) => item.generationStatus === 'pending' || item.generationStatus === 'in_progress'
		).length ?? 0
	);
	const progressPercentage = $derived(totalPosts > 0 ? (completedPosts / totalPosts) * 100 : 0);
</script>

<div class="w-full min-h-[400px]">
	{#if hasItems && contentPlanItems}
		<div class="space-y-4 h-full" in:fly={{ y: 30, duration: 600 }}>
			{#if totalPosts > 0}
				<div class="space-y-2">
					<div class="flex items-center justify-between">
						<span class="text-sm font-medium">
							Posts: {completedPosts}/{totalPosts} completed
						</span>
						{#if loadingPosts > 0}
							<span class="text-sm text-muted-foreground flex items-center gap-1.5">
								<Loader2 class="w-3 h-3 animate-spin" />
								{loadingPosts} generating
							</span>
						{/if}
					</div>
					<div class="w-full bg-muted rounded-full h-2 overflow-hidden">
						<div
							class="h-full bg-primary transition-all duration-500 ease-out"
							style="width: {progressPercentage}%"
						></div>
					</div>
				</div>
			{/if}
			{#if brandId && jobId}
				<CampaignCreationCalendar
					{contentPlanItems}
					{brandName}
					brandId={brandId}
					jobId={jobId}
				/>
			{/if}
		</div>
	{:else if isJobActive}
		<div class="space-y-3" in:fly={{ y: 20, duration: 500 }}>
			<div class="flex items-center gap-2 text-sm text-muted-foreground mb-4">
				<Loader2 class="w-4 h-4 animate-spin" />
				<span>Building content plan…</span>
			</div>
			{#each { length: 5 } as _, i}
				<div
					class="h-14 rounded-lg bg-muted animate-pulse"
					style="animation-delay: {i * 80}ms; opacity: {1 - i * 0.15}"
					in:fly={{ y: 10, duration: 300, delay: i * 60 }}
				></div>
			{/each}
		</div>
	{:else}
		<div class="flex items-center justify-center h-64">
			<Card class="border border-border max-w-md">
				<CardContent class="p-8 text-center">
					<p class="text-muted-foreground text-sm">No content plan available.</p>
				</CardContent>
			</Card>
		</div>
	{/if}
</div>

