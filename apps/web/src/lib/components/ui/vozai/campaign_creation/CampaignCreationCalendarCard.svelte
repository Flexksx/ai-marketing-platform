<script lang="ts">
	import type { CampaignContentPlanItem } from '$lib/api/campaign-generation-jobs';
	import type { ContentPreviewItem } from '$lib/api/content/ContentPreviewItem';
	import CalendarContentPreviewCardLarge from '$lib/components/content/CalendarContentPreviewCardLarge.svelte';
	import { Badge } from '$lib/components/ui/badge';
	import { Loader2, CheckCircle2, AlertCircle } from 'lucide-svelte';

	type Props = {
		planItem: CampaignContentPlanItem;
		compact?: boolean;
		onclick?: () => void;
	};

	let { planItem, compact = false, onclick }: Props = $props();

	const getStatusBadge = (item: CampaignContentPlanItem) => {
		switch (item.generationStatus) {
			case 'completed':
				return {
					variant: 'outline' as const,
					class:
						'text-xs bg-green-50 dark:bg-green-950 border-green-300 dark:border-green-700 text-green-700 dark:text-green-300',
					icon: CheckCircle2,
					text: 'Post Ready'
				};
			case 'failed':
				return {
					variant: 'outline' as const,
					class:
						'text-xs bg-red-50 dark:bg-red-950 border-red-300 dark:border-red-700 text-red-700 dark:text-red-300',
					icon: AlertCircle,
					text: 'Failed'
				};
			default:
				return {
					variant: 'outline' as const,
					class:
						'text-xs bg-amber-50 dark:bg-amber-950 border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300',
					icon: Loader2,
					text: 'Generating...'
				};
		}
	};

	const previewItem = $derived<ContentPreviewItem>({
		caption: planItem.contentData?.caption ?? planItem.description,
		mediaUrl: planItem.imageUrls?.[0] ?? null,
		channel: planItem.channel,
		scheduledAt: planItem.scheduledAt
	});

	const statusBadge = $derived(getStatusBadge(planItem));
</script>

<div class="relative">
	<CalendarContentPreviewCardLarge
		post={previewItem}
		viewMode="month"
		{onclick}
	/>
	<div class="absolute top-1 right-1 z-10 pointer-events-none">
		<Badge variant={statusBadge.variant} class={statusBadge.class}>
			<svelte:component
				this={statusBadge.icon}
				class="w-2 h-2 {statusBadge.icon === Loader2 ? 'animate-spin' : ''}"
			/>
		</Badge>
	</div>
</div>
