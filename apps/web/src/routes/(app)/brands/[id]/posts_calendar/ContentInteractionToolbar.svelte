<script lang="ts">
	import { page } from '$app/state';
	import { JobStatus } from '$lib/api/job/JobStatus';
	import { useContentGenerationJob } from '$lib/api/content-generation-jobs/queries';
	import CampaignCreationDialog from '$lib/components/campaign/CampaignCreationDialog.svelte';
	import ContentGenerationJobDialog from '$lib/components/content/creation/ContentGenerationJobDialog.svelte';
	import type { ContentGenerationJobDialogState } from '$lib/components/content/creation/content-generation-job-dialog-state';
	import CalendarToolbar from '$lib/components/ui/vozai/calendar/CalendarToolbar.svelte';
	import OnboardedCalendarCTA from './OnboardedCalendarCTA.svelte';

	let { brandId = '' }: { brandId: string } = $props();

	const isOnboarded = $derived(page.url.searchParams.get('onboarded') === 'true');

	let showCampaignDialog = $state(false);
	let showContentDialog = $state(false);
	let contentGenerationJobId = $state<string | null>(null);

	const brand = $derived(brandId ? { id: brandId } : null);

	const jobQuery = useContentGenerationJob(
		() => brandId,
		() => contentGenerationJobId ?? undefined
	);

	const isPolling = $derived(
		!!contentGenerationJobId &&
			(!jobQuery.data ||
				jobQuery.data.status === JobStatus.PENDING ||
				jobQuery.data.status === JobStatus.IN_PROGRESS)
	);
	const isComplete = $derived(jobQuery.data?.status === JobStatus.COMPLETED);
	const isFailed = $derived(jobQuery.data?.status === JobStatus.FAILED);

	const contentJobState = $derived<ContentGenerationJobDialogState>(
		!contentGenerationJobId
			? 'idle'
			: isPolling
				? 'polling'
				: isFailed
					? 'failed'
					: isComplete
						? 'complete'
						: 'idle'
	);
</script>

{#if brandId}
	{#if isOnboarded}
		<OnboardedCalendarCTA
			onCreateCampaign={() => (showCampaignDialog = true)}
			onCreateContent={() => (showContentDialog = true)}
		/>
	{:else}
		<CalendarToolbar
			{contentJobState}
			onCreateCampaign={() => (showCampaignDialog = true)}
			onCreateContent={() => (showContentDialog = true)}
		/>
	{/if}
{/if}

{#if brand}
	<CampaignCreationDialog {brand} bind:open={showCampaignDialog} />
	<ContentGenerationJobDialog
		{brand}
		bind:open={showContentDialog}
		bind:contentGenerationJobId
		jobResult={jobQuery.data?.result ?? null}
		{isPolling}
		{isComplete}
		{isFailed}
	/>
{/if}
