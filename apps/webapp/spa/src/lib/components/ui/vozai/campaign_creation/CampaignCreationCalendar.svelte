<script lang="ts">
	import { SvelteDate, SvelteSet } from 'svelte/reactivity';
	import { Button } from '$lib/components/ui/button';
	import type { CampaignContentPlanItem } from '$lib/api/campaign-generation-jobs';
	import { useUpdateContentPlanItem } from '$lib/api/campaign-generation-jobs/mutations';
	import CampaignCreationCalendarCard from './CampaignCreationCalendarCard.svelte';
	import CampaignContentPlanItemDialog from './CampaignContentPlanItemDialog.svelte';
	import instagramLogo from '$lib/assets/instagram_logo.png';
	import linkedinLogo from '$lib/assets/linkedin_logo.png';

	type Props = {
		contentPlanItems: CampaignContentPlanItem[];
		brandName: string;
		brandId: string;
		jobId: string;
	};

	let { contentPlanItems, brandName, brandId, jobId }: Props = $props();

	type PostChannel = 'INSTAGRAM' | 'LINKEDIN';

	let selectedChannels = new SvelteSet<PostChannel>(['INSTAGRAM', 'LINKEDIN']);
	let selectedItem = $state<CampaignContentPlanItem | null>(null);
	let dialogOpen = $state(false);

	const updateMutation = useUpdateContentPlanItem();

	let draggingItemId = $state<string | null>(null);
	let dropTargetDayKey = $state<string | null>(null);
	let dropTargetIndex = $state<number | null>(null);

	const dayKey = (date: Date) => {
		const yyyy = date.getFullYear();
		const mm = String(date.getMonth() + 1).padStart(2, '0');
		const dd = String(date.getDate()).padStart(2, '0');
		return `${yyyy}-${mm}-${dd}`;
	};

	const parseTimeMs = (iso: string) => new Date(iso).getTime();
	const toIso = (ms: number) => new Date(ms).toISOString();

	const clampToDay = (ms: number, day: Date) => {
		const start = new Date(day);
		start.setHours(0, 0, 0, 0);
		const end = new Date(day);
		end.setHours(23, 59, 59, 999);
		return Math.min(end.getTime(), Math.max(start.getTime(), ms));
	};

	const midpoint = (a: number, b: number) => Math.floor((a + b) / 2);

	const compareItems = (a: CampaignContentPlanItem, b: CampaignContentPlanItem) => {
		const diff = parseTimeMs(a.scheduledAt) - parseTimeMs(b.scheduledAt);
		if (diff !== 0) return diff;
		return a.id.localeCompare(b.id);
	};

	const getCampaignDateRange = () => {
		if (contentPlanItems.length === 0) {
			return { startDate: new Date(), endDate: new Date() };
		}

		const times = contentPlanItems.map((item) => new Date(item.scheduledAt).getTime());
		const firstItemDate = new SvelteDate(Math.min(...times));
		const lastItemDate = new SvelteDate(Math.max(...times));

		firstItemDate.setHours(0, 0, 0, 0);
		lastItemDate.setHours(0, 0, 0, 0);

		const startDate = new SvelteDate(firstItemDate);
		startDate.setDate(startDate.getDate() - startDate.getDay());

		const endDate = new SvelteDate(lastItemDate);
		endDate.setDate(endDate.getDate() + (6 - endDate.getDay()));
		endDate.setDate(endDate.getDate() + 7);

		return { startDate, endDate };
	};

	const formatCampaignRange = (startDate: Date, endDate: Date): string => {
		const startMonth = startDate.toLocaleDateString('en-US', { month: 'short' });
		const endMonth = endDate.toLocaleDateString('en-US', { month: 'short' });
		const startDay = startDate.getDate();
		const endDay = endDate.getDate();
		const startYear = startDate.getFullYear();
		const endYear = endDate.getFullYear();

		if (startYear === endYear) {
			if (startMonth === endMonth) {
				return `${startMonth} ${startDay} - ${endDay}, ${startYear}`;
			}
			return `${startMonth} ${startDay} - ${endMonth} ${endDay}, ${startYear}`;
		}
		return `${startMonth} ${startDay}, ${startYear} - ${endMonth} ${endDay}, ${endYear}`;
	};

	const getCampaignDays = (startDate: Date, endDate: Date): Date[] => {
		const days: Date[] = [];
		const currentDate = new SvelteDate(startDate);

		const firstDayOfWeek = currentDate.getDay();
		for (let i = firstDayOfWeek - 1; i >= 0; i--) {
			const paddingDate = new SvelteDate(startDate);
			paddingDate.setDate(paddingDate.getDate() - (i + 1));
			days.push(paddingDate);
		}

		while (currentDate <= endDate) {
			days.push(new SvelteDate(currentDate));
			currentDate.setDate(currentDate.getDate() + 1);
		}

		const lastDayOfWeek = days[days.length - 1].getDay();
		const paddingEnd = lastDayOfWeek === 6 ? 0 : 6 - lastDayOfWeek;

		for (let i = 1; i <= paddingEnd; i++) {
			const paddingDate = new SvelteDate(endDate);
			paddingDate.setDate(paddingDate.getDate() + i);
			days.push(paddingDate);
		}

		const rowsNeeded = Math.ceil(days.length / 7);
		const totalCells = rowsNeeded * 7;
		const extraPadding = totalCells - days.length;

		for (let i = 1; i <= extraPadding; i++) {
			const paddingDate = new SvelteDate(days[days.length - 1]);
			paddingDate.setDate(paddingDate.getDate() + 1);
			days.push(paddingDate);
		}

		return days;
	};

	const getItemsForDate = (date: Date): CampaignContentPlanItem[] => {
		return [...contentPlanItems]
			.filter((item) => {
				if (!selectedChannels.has(item.channel as PostChannel)) return false;

				const itemDate = new Date(item.scheduledAt);
				return (
					itemDate.getDate() === date.getDate() &&
					itemDate.getMonth() === date.getMonth() &&
					itemDate.getFullYear() === date.getFullYear()
				);
			})
			.sort(compareItems);
	};

	const isInCampaignRange = (date: Date, startDate: Date, endDate: Date): boolean => {
		return date >= startDate && date <= endDate;
	};

	const isToday = (date: Date): boolean => {
		const today = new Date();
		return (
			date.getDate() === today.getDate() &&
			date.getMonth() === today.getMonth() &&
			date.getFullYear() === today.getFullYear()
		);
	};

	const toggleChannel = (channel: PostChannel) => {
		if (selectedChannels.has(channel)) {
			selectedChannels.delete(channel);
		} else {
			selectedChannels.add(channel);
		}
	};

	const selectAllChannels = () => {
		selectedChannels.clear();
		selectedChannels.add('INSTAGRAM');
		selectedChannels.add('LINKEDIN');
	};

	const getChannelLogo = (channel: PostChannel): string => {
		switch (channel) {
			case 'INSTAGRAM':
				return instagramLogo;
			case 'LINKEDIN':
				return linkedinLogo;
			default:
				return '';
		}
	};

	const campaignRange = $derived(getCampaignDateRange());
	const campaignDays = $derived(getCampaignDays(campaignRange.startDate, campaignRange.endDate));
	const displayTitle = $derived(
		formatCampaignRange(campaignRange.startDate, campaignRange.endDate)
	);

	const ITEMS_PER_CELL = 3;

	const computeScheduledAtForDrop = (
		targetDay: Date,
		targetIndex: number,
		targetDayItems: CampaignContentPlanItem[],
		movedItemId: string
	) => {
		const items = [...targetDayItems].filter((i) => i.id !== movedItemId).sort(compareItems);

		if (items.length === 0) {
			const t = new Date(targetDay);
			t.setHours(9, 0, 0, 0);
			return toIso(clampToDay(t.getTime(), targetDay));
		}

		const clampedIndex = Math.min(Math.max(0, targetIndex), items.length);
		const prev = items[clampedIndex - 1];
		const next = items[clampedIndex];
		const ONE_MINUTE_MS = 60_000;

		if (prev && next) {
			return toIso(
				clampToDay(midpoint(parseTimeMs(prev.scheduledAt), parseTimeMs(next.scheduledAt)), targetDay)
			);
		}

		if (prev) return toIso(clampToDay(parseTimeMs(prev.scheduledAt) + ONE_MINUTE_MS, targetDay));

		return toIso(clampToDay(parseTimeMs(next.scheduledAt) - ONE_MINUTE_MS, targetDay));
	};

	const startDrag = (event: DragEvent, item: CampaignContentPlanItem, day: Date) => {
		draggingItemId = item.id;
		dropTargetDayKey = dayKey(day);
		dropTargetIndex = null;

		event.dataTransfer?.setData('text/plain', item.id);
		if (event.dataTransfer) event.dataTransfer.effectAllowed = 'move';
	};

	const clearDrag = () => {
		draggingItemId = null;
		dropTargetDayKey = null;
		dropTargetIndex = null;
	};

	const allowDrop = (event: DragEvent, day: Date, index: number | null) => {
		event.preventDefault();
		if (!draggingItemId && !event.dataTransfer?.getData('text/plain')) return;
		dropTargetDayKey = dayKey(day);
		dropTargetIndex = index;
		if (event.dataTransfer) event.dataTransfer.dropEffect = 'move';
	};

	const dropOnDay = (event: DragEvent, day: Date, index: number) => {
		event.preventDefault();
		const itemId = draggingItemId ?? event.dataTransfer?.getData('text/plain') ?? null;
		if (!itemId) return clearDrag();

		const targetDayItems = getItemsForDate(day);
		const scheduledAt = computeScheduledAtForDrop(day, index, targetDayItems, itemId);

		updateMutation.mutate({
			brandId,
			jobId,
			itemId,
			modification: {
				item_id: itemId,
				scheduled_at: scheduledAt
			}
		});

		clearDrag();
	};
</script>

<div class="flex h-full w-full">
	<div class="flex-1 flex flex-col overflow-hidden">
		<div class="bg-card flex flex-col overflow-hidden">
			<div class="mb-6 flex shrink-0 items-center justify-between">
				<div class="flex items-center space-x-4">
					<div class="text-center min-w-[300px]">
						<h2 class="text-xl font-semibold">{displayTitle}</h2>
						<p class="text-sm text-muted-foreground">Campaign Duration</p>
					</div>
				</div>
				<div class="flex items-center gap-3">
					<div class="flex items-center gap-2">
						<span class="text-sm text-muted-foreground mr-2">Filter:</span>
						<Button
							variant={selectedChannels.has('INSTAGRAM') ? 'default' : 'outline'}
							size="sm"
							onclick={() => toggleChannel('INSTAGRAM')}
							class="p-2"
							title="Instagram"
						>
							<img src={getChannelLogo('INSTAGRAM')} alt="Instagram" class="h-4 w-4" />
						</Button>
						<Button
							variant={selectedChannels.has('LINKEDIN') ? 'default' : 'outline'}
							size="sm"
							onclick={() => toggleChannel('LINKEDIN')}
							class="p-2"
							title="LinkedIn"
						>
							<img src={getChannelLogo('LINKEDIN')} alt="LinkedIn" class="h-4 w-4" />
						</Button>
						<Button
							variant={selectedChannels.size === 2 ? 'default' : 'outline'}
							size="sm"
							onclick={selectAllChannels}
						>
							All
						</Button>
					</div>
				</div>
			</div>

			<div class="grid min-h-0 flex-1 grid-cols-7 gap-3 overflow-hidden">
				<div class="text-center font-semibold text-sm py-2">Sun</div>
				<div class="text-center font-semibold text-sm py-2">Mon</div>
				<div class="text-center font-semibold text-sm py-2">Tue</div>
				<div class="text-center font-semibold text-sm py-2">Wed</div>
				<div class="text-center font-semibold text-sm py-2">Thu</div>
				<div class="text-center font-semibold text-sm py-2">Fri</div>
				<div class="text-center font-semibold text-sm py-2">Sat</div>

				{#each campaignDays as day (day.getTime())}
					{@const dayItems = getItemsForDate(day)}
					{@const visibleItems = dayItems.slice(0, ITEMS_PER_CELL)}
					{@const inRange = isInCampaignRange(day, campaignRange.startDate, campaignRange.endDate)}
					{@const currentDayKey = dayKey(day)}
					<div
						class="flex flex-col min-h-[120px] border rounded p-2 {inRange ? 'bg-background' : 'bg-muted/30'} {dropTargetDayKey === currentDayKey
							? 'ring-2 ring-primary/30'
							: ''}"
						ondragover={(e) => allowDrop(e, day, dayItems.length)}
						ondrop={(e) => dropOnDay(e, day, dropTargetIndex ?? dayItems.length)}
					>
						<div class="mb-1 flex items-center justify-between">
							<span
								class="text-sm font-semibold {isToday(day)
									? 'bg-primary text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-xs'
									: inRange
										? 'text-foreground'
										: 'text-muted-foreground'}"
							>
								{day.getDate()}
							</span>
						</div>
						<div class="flex-1 space-y-1 overflow-hidden">
							<div
								class="h-1 rounded {dropTargetDayKey === currentDayKey && dropTargetIndex === 0
									? 'bg-primary/40'
									: 'bg-transparent'}"
								ondragover={(e) => allowDrop(e, day, 0)}
								ondrop={(e) => dropOnDay(e, day, 0)}
							></div>
							{#each visibleItems as item, i (item.id)}
								<div
									draggable={true}
									class="rounded {draggingItemId === item.id ? 'opacity-60' : ''}"
									ondragstart={(e) => startDrag(e, item, day)}
									ondragend={clearDrag}
								>
									<CampaignCreationCalendarCard
										planItem={item}
										compact={true}
										onclick={() => {
											if (draggingItemId) return;
											selectedItem = item;
											dialogOpen = true;
										}}
									/>
								</div>
								<div
									class="h-1 rounded {dropTargetDayKey === currentDayKey && dropTargetIndex === i + 1
										? 'bg-primary/40'
										: 'bg-transparent'}"
									ondragover={(e) => allowDrop(e, day, i + 1)}
									ondrop={(e) => dropOnDay(e, day, i + 1)}
								></div>
							{/each}
							{#if dayItems.length > ITEMS_PER_CELL}
								<div
									class="text-[10px] text-center py-0.5 rounded {dropTargetDayKey === currentDayKey && dropTargetIndex !== null
										? 'bg-primary/10 text-primary'
										: 'text-muted-foreground'}"
									ondragover={(e) => allowDrop(e, day, dayItems.length)}
									ondrop={(e) => dropOnDay(e, day, dayItems.length)}
								>
									+{dayItems.length - ITEMS_PER_CELL}
								</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

{#if selectedItem}
	{#key selectedItem.id}
		<CampaignContentPlanItemDialog
			bind:open={dialogOpen}
			selectedItem={selectedItem}
			{brandName}
			{brandId}
			{jobId}
			onDeleted={() => {
				dialogOpen = false;
				selectedItem = null;
			}}
		/>
	{/key}
{/if}
