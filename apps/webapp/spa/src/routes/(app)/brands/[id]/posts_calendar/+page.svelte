<script lang="ts">
	import { page } from '$app/state';
	import type { Content } from '$lib/api/content/Content';
	import CalendarContentPreviewCardLarge from '$lib/components/content/CalendarContentPreviewCardLarge.svelte';
	import CampaignContentDialog from '$lib/components/content/CampaignContentDialog.svelte';
	import * as Dialog from '$lib/components/ui/dialog';
	import { SvelteDate } from 'svelte/reactivity';
	import ContentCalendarControls from './ContentCalendarControls.svelte';
	import ContentInteractionToolbar from './ContentInteractionToolbar.svelte';
	import MonthlyContentCalendar from './MonthlyContentCalendar.svelte';
	import WeeklyContentCalendar from './WeeklyContentCalendar.svelte';

	const brandId = $derived(page.params.id);

	type CalendarViewMode = 'week' | 'month';

	let viewMode = $state<CalendarViewMode>('week');

	const getStartOfWeek = (date: Date = new Date()): Date => {
		const d = new SvelteDate(date);
		d.setHours(0, 0, 0, 0);
		const day = d.getDay();
		const diff = d.getDate() - day + (day === 0 ? -6 : 1);
		const startOfWeek = new SvelteDate(d);
		startOfWeek.setDate(diff);
		return startOfWeek;
	};

	const getStartOfMonth = (date: Date = new Date()): Date => {
		const d = new SvelteDate(date);
		d.setHours(0, 0, 0, 0);
		d.setDate(1);
		return d;
	};

	let currentWeekStart = $state(getStartOfWeek(new SvelteDate()));
	let currentMonthStart = $state(getStartOfMonth(new SvelteDate()));
	let slideDirection = $state<'left' | 'right' | null>(null);

	let dialogOpen = $state(false);
	let dialogContent = $state<Content[]>([]);
	let dialogDate = $state<SvelteDate | null>(null);
	let selectedContent = $state<Content | null>(null);

	const openDialog = (content: Content[], date: Date) => {
		const sorted = [...content].sort((a, b) => {
			if (!a.scheduledAt && !b.scheduledAt) return 0;
			if (!a.scheduledAt) return 1;
			if (!b.scheduledAt) return -1;
			return new SvelteDate(a.scheduledAt).getTime() - new SvelteDate(b.scheduledAt).getTime();
		});
		dialogContent = sorted;
		dialogDate = new SvelteDate(date);
		dialogOpen = true;
	};

	const openContentDialog = (content: Content) => {
		selectedContent = content;
	};

	const formatDialogDate = (date: SvelteDate): string => {
		return date.toLocaleDateString('en-US', {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	};
</script>

<div class="w-full h-full flex flex-col">
	<div class="flex-1 flex flex-col px-8 py-4 overflow-hidden">
		<div class="bg-card rounded-2xl border p-4 shadow-sm flex-1 flex flex-col overflow-hidden">
			<ContentCalendarControls
				bind:viewMode
				bind:currentWeekStart
				bind:currentMonthStart
				bind:slideDirection
			/>

			{#if viewMode === 'week'}
				<WeeklyContentCalendar
					brandId={brandId ?? ''}
					weekStart={currentWeekStart}
					{slideDirection}
					onOpenMore={openDialog}
					onPostClick={openContentDialog}
				/>
			{:else}
				<MonthlyContentCalendar
					brandId={brandId ?? ''}
					monthStart={currentMonthStart}
					onOpenMore={openDialog}
					onPostClick={openContentDialog}
				/>
			{/if}
		</div>
	</div>
</div>

<Dialog.Root bind:open={dialogOpen}>
	<Dialog.Content class="max-w-4xl max-h-[90vh] flex flex-col">
		<Dialog.Header class="flex-shrink-0">
			<Dialog.Title>
				{#if dialogDate}
					Posts for {formatDialogDate(dialogDate)}
				{:else}
					All Posts
				{/if}
			</Dialog.Title>
		</Dialog.Header>
		<div class="flex-1 min-h-0 overflow-y-auto">
			<div class="grid grid-cols-2 md:grid-cols-3 gap-4 pb-4">
				{#each dialogContent as post (post.id)}
					<CalendarContentPreviewCardLarge
						{post}
						viewMode="week"
						onclick={() => openContentDialog(post)}
					/>
				{/each}
			</div>
		</div>
	</Dialog.Content>
</Dialog.Root>

{#if selectedContent}
	<CampaignContentDialog
		post={selectedContent}
		open={selectedContent}
		onClose={() => (selectedContent = null)}
	/>
{/if}

<ContentInteractionToolbar brandId={brandId ?? ''} />
