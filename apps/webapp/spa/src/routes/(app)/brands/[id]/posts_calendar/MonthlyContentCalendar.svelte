<script lang="ts">
	import type { Content } from '$lib/api/content/Content';
	import { useContentForBrand } from '$lib/api/content/queries';
	import CalendarContentPreviewCardLarge from '$lib/components/content/CalendarContentPreviewCardLarge.svelte';
	import { Button } from '$lib/components/ui/button';
	import { SvelteDate, SvelteMap } from 'svelte/reactivity';
	import MonthlyCalendarDayHeading from './MonthlyCalendarDayHeading.svelte';

	type Props = {
		brandId: string;
		monthStart: Date;
		onOpenMore?: (content: Content[], date: Date) => void;
		onPostClick?: (content: Content) => void;
	};

	let { brandId, monthStart, onOpenMore, onPostClick }: Props = $props();

	const contentQuery = useContentForBrand(
		() => brandId,
		() => ({ limit: 100, offset: 0 })
	);

	const content = $derived(contentQuery.data ?? []);
	const isLoading = $derived(contentQuery.isLoading);
	const errorMessage = $derived(contentQuery.error?.message ?? null);

	const getMonthDays = (startDate: Date): Date[] => {
		const days: Date[] = [];
		const year = startDate.getFullYear();
		const month = startDate.getMonth();

		const firstDay = new SvelteDate(year, month, 1);
		const lastDay = new SvelteDate(year, month + 1, 0);

		const startDayOfWeek = firstDay.getDay();
		const startOffset = startDayOfWeek === 0 ? 6 : startDayOfWeek - 1;

		const endDayOfWeek = lastDay.getDay();
		const endOffset = endDayOfWeek === 0 ? 0 : 7 - endDayOfWeek;

		const totalDays = lastDay.getDate() + startOffset + endOffset;

		for (let i = 0; i < totalDays; i++) {
			const day = new SvelteDate(year, month, 1 - startOffset + i);
			days.push(day);
		}

		return days;
	};

	const isCurrentMonth = (date: Date, currentMonth: Date): boolean => {
		return (
			date.getMonth() === currentMonth.getMonth() &&
			date.getFullYear() === currentMonth.getFullYear()
		);
	};

	const contentByDateMap = $derived(() => {
		const map = new SvelteMap<string, Content[]>();
		for (const item of content) {
			if (item.scheduledAt) {
				const dateStr = new SvelteDate(item.scheduledAt).toISOString().split('T')[0];
				if (!map.has(dateStr)) {
					map.set(dateStr, []);
				}
				map.get(dateStr)!.push(item);
			}
		}
		return map;
	});

	const getContentForDate = (date: Date): Content[] => {
		const targetDateStr = new SvelteDate(date).toISOString().split('T')[0]!;
		return contentByDateMap().get(targetDateStr) ?? [];
	};

	const monthDays = $derived(getMonthDays(monthStart));

	const POSTS_PER_COLUMN = 5;
</script>

{#if isLoading}
	<div class="text-center py-8 flex-1 flex items-center justify-center">Loading content...</div>
{:else if errorMessage}
	<div class="text-center py-8 text-red-500 flex-1 flex items-center justify-center">
		Error: {errorMessage}
	</div>
{:else}
	<div class="flex-1 overflow-y-auto">
		<div class="grid grid-cols-7 gap-2">
			<div class="text-center font-semibold text-sm py-2">Sun</div>
			<div class="text-center font-semibold text-sm py-2">Mon</div>
			<div class="text-center font-semibold text-sm py-2">Tue</div>
			<div class="text-center font-semibold text-sm py-2">Wed</div>
			<div class="text-center font-semibold text-sm py-2">Thu</div>
			<div class="text-center font-semibold text-sm py-2">Fri</div>
			<div class="text-center font-semibold text-sm py-2">Sat</div>

			{#each monthDays as day (day.getTime())}
				{@const dayContent = getContentForDate(day)}
				{@const visibleContent = dayContent.slice(0, POSTS_PER_COLUMN)}
				{@const hiddenContent = dayContent.slice(POSTS_PER_COLUMN)}
				<div
					class="flex flex-col min-h-[250px] border rounded p-2 {isCurrentMonth(day, monthStart)
						? 'bg-background'
						: 'bg-muted/30'}"
				>
					<div class="mb-1 flex items-center justify-between">
						<MonthlyCalendarDayHeading
							date={new SvelteDate(day)}
							currentDate={new SvelteDate()}
							isInView={isCurrentMonth(day, monthStart)}
						/>
					</div>
					<div class="flex-1 space-y-1.5 overflow-hidden text-xs">
						{#each visibleContent as post (post.id)}
							<CalendarContentPreviewCardLarge
								{post}
								viewMode="month"
								onclick={() => onPostClick?.(post)}
							/>
						{/each}
						{#if hiddenContent.length > 0 && onOpenMore}
							<Button
								variant="outline"
								size="sm"
								class="w-full mt-1.5 text-xs h-6"
								onclick={() => onOpenMore(dayContent, day)}
							>
								({hiddenContent.length} More)
							</Button>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	</div>
{/if}
