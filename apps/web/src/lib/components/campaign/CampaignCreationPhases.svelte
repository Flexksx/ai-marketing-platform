<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import type {
		CampaignGenerationJobResult,
		ContentBriefCampaignGenerationJobResult
	} from '$lib/api/campaign-generation-jobs';
	import { useAcceptCampaignGenerationJob } from '$lib/api/campaign-generation-jobs/mutations';
	import { useBrand } from '$lib/api/brands/queries';
	import { queryKeys } from '$lib/api/shared/queryKeys';
	import { useQueryClient } from '@tanstack/svelte-query';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import CampaignCreationJobContentPlanTab from '$lib/components/ui/vozai/campaign_creation/CampaignCreationJobContentPlanTab.svelte';
	import CampaignCreationJobOverviewTab from '$lib/components/ui/vozai/campaign_creation/CampaignCreationJobOverviewTab.svelte';
	import { navigate } from '$lib/navigation';
	import { ChevronLeft, Loader2 } from 'lucide-svelte';
	import { fade, fly } from 'svelte/transition';
	import { JobStatus } from '$lib/api/job/JobStatus';

	type Props = {
		result: CampaignGenerationJobResult | null;
		brandName: string;
		brandLogoUrl?: string | null;
		jobStatus?: JobStatus;
		jobId?: string;
		brandId?: string;
	};

	let {
		result,
		brandName,
		brandLogoUrl = null,
		jobStatus = JobStatus.PENDING,
		jobId,
		brandId
	}: Props = $props();

	const brandIdFromPage = $derived(brandId || page.params.id);

	const queryClient = useQueryClient();
	const acceptJobMutation = useAcceptCampaignGenerationJob();
	const brandQuery = useBrand(() => brandIdFromPage || undefined);

	const audiences = $derived(brandQuery.data?.data?.audiences ?? []);
	const contentPillars = $derived(brandQuery.data?.data?.contentPillars ?? []);

	const brief = $derived<ContentBriefCampaignGenerationJobResult | null>(
		result?.content_brief ?? null
	);
	const contentPlanItems = $derived(result?.content_plan_items ?? null);
	const isJobActive = $derived(
		jobStatus === JobStatus.PENDING || jobStatus === JobStatus.IN_PROGRESS
	);
	const isLoading = $derived(isJobActive && !brief);

	const statusVariant = $derived((): 'default' | 'secondary' | 'destructive' | 'outline' => {
		if (jobStatus === JobStatus.COMPLETED || jobStatus === JobStatus.ACCEPTED) return 'default';
		if (jobStatus === JobStatus.FAILED || jobStatus === JobStatus.CANCELLED) return 'destructive';
		return 'secondary';
	});

	const canApproveAndSchedule = $derived(
		Boolean(
			brandIdFromPage &&
				jobId &&
				(jobStatus === JobStatus.COMPLETED || jobStatus === JobStatus.ACCEPTED)
		)
	);
	const isAccepting = $derived(acceptJobMutation.isPending);

	const handleApproveAndSchedule = () => {
		if (!brandIdFromPage || !jobId || !canApproveAndSchedule) return;
		acceptJobMutation.mutate(
			{
				brandId: brandIdFromPage,
				jobId,
				request: {}
			},
			{
				onSuccess: () => {
					queryClient.invalidateQueries({ queryKey: queryKeys.campaignGenerationJob(jobId) });
					navigate(resolve(`/brands/${brandIdFromPage}/posts_calendar`));
				}
			}
		);
	};

	const handleDiscard = () => {
		if (!brandIdFromPage) return;
		if (confirm('Are you sure you want to go back?')) {
			navigate(resolve(`/brands/${brandIdFromPage}/posts_calendar`));
		}
	};
</script>

<div class="w-full h-full">
	<div class="w-[95%] max-w-[1800px] mx-auto px-8 py-8">
		<div class="mb-8" in:fly={{ y: -20, duration: 600 }}>
			<div class="flex flex-wrap items-center gap-4 mb-2">
				<Button variant="ghost" size="icon" onclick={handleDiscard}>
					<ChevronLeft class="h-5 w-5" />
				</Button>
				{#if brandLogoUrl}
					<div
						class="h-12 w-12 rounded-full overflow-hidden shadow border border-border bg-background p-1.5 flex-shrink-0"
					>
						<img src={brandLogoUrl} alt={brandName || 'Brand'} class="h-full w-full object-contain" />
					</div>
				{/if}
				{#if brandName}
					<h1 class="text-2xl md:text-3xl font-bold text-foreground flex-1">{brandName}</h1>
				{/if}
				{#if jobStatus}
					<Badge variant={statusVariant()} class="capitalize">
						{jobStatus.replace('_', ' ')}
					</Badge>
				{/if}
				<div class="flex items-center gap-2 ml-auto">
					<Button variant="outline" onclick={handleDiscard}>Discard</Button>
					<Button
						disabled={!canApproveAndSchedule || isAccepting}
						onclick={handleApproveAndSchedule}
					>
						{#if isAccepting}
							<Loader2 class="h-4 w-4 animate-spin" />
						{/if}
						Approve & Schedule
					</Button>
				</div>
			</div>
		</div>

		{#if jobStatus === 'failed'}
			<div class="mt-8 text-center" in:fade>
				<div class="border-2 border-destructive/50 bg-destructive/5 rounded-lg p-8">
					<p class="text-lg text-destructive mb-4 font-semibold">Content plan generation failed</p>
					<p class="text-muted-foreground mb-6">
						Something went wrong while generating your content plan. Please try again.
					</p>
					<Button
						variant="destructive"
						onclick={() => {
							navigate(resolve(`/brands/${brandIdFromPage}`));
						}}
					>
						Back to Brand
					</Button>
				</div>
			</div>
		{:else}
			<div class="space-y-12">
				<CampaignCreationJobOverviewTab
					{brief}
					{audiences}
					{contentPillars}
					{isLoading}
					{isJobActive}
				/>
				{#if brief}
					<CampaignCreationJobContentPlanTab
						{contentPlanItems}
						{brandName}
						{isJobActive}
						brandId={brandIdFromPage}
						{jobId}
					/>
				{/if}
			</div>
		{/if}
	</div>
</div>
