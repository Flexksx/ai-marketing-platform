<script lang="ts">
	import type { Content } from '$lib/api/content/Content';
	import { useContentForBrand } from '$lib/api/content/queries';
	import CalendarContentPreviewCardLarge from '$lib/components/content/CalendarContentPreviewCardLarge.svelte';
	import { Button } from '$lib/components/ui/button';
	import { SvelteDate, SvelteMap } from 'svelte/reactivity';
	import { fly } from 'svelte/transition';
	import WeeklyCalendarDayHeading from './WeeklyCalendarDayHeading.svelte';

	type Props = {
		brandId: string;
		weekStart: Date;
		slideDirection: 'left' | 'right' | null;
		onOpenMore?: (content: Content[], date: Date) => void;
		onPostClick?: (content: Content) => void;
	};

	let { brandId, weekStart, slideDirection, onOpenMore, onPostClick }: Props = $props();

	const contentQuery = useContentForBrand(
		() => brandId,
		() => ({ limit: 100, offset: 0 })
	);

	const content = $derived(contentQuery.data ?? []);
	const isLoading = $derived(contentQuery.isLoading);
	const errorMessage = $derived(contentQuery.error?.message ?? null);

	const getWeekDays = (startDate: Date): Date[] => {
		const days: Date[] = [];
		for (let i = 0; i < 7; i++) {
			const date = new SvelteDate(startDate);
			date.setDate(date.getDate() + i);
			days.push(date);
		}
		return days;
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

	const weekDays = $derived(getWeekDays(weekStart));

	const POSTS_PER_COLUMN = 5;
	const CARD_HEIGHT_WEEK = 240;
	const CARD_SPACING = 8;
	const COLUMN_HEIGHT_WEEK =
		POSTS_PER_COLUMN * CARD_HEIGHT_WEEK + (POSTS_PER_COLUMN - 1) * CARD_SPACING;
</script>

{#if isLoading}
	<div class="text-center py-8 flex-1 flex items-center justify-center">Loading content...</div>
{:else if errorMessage}
	<div class="text-center py-8 text-red-500 flex-1 flex items-center justify-center">
		Error: {errorMessage}
	</div>
{:else}
	<div class="flex-1 overflow-y-auto">
		{#key weekStart.getTime()}
			<div
				class="grid grid-cols-7 gap-4"
				in:fly={{
					x: slideDirection === 'left' ? 300 : slideDirection === 'right' ? -300 : 0,
					duration: 300
				}}
				out:fly={{
					x: slideDirection === 'left' ? -300 : slideDirection === 'right' ? 300 : 0,
					duration: 300
				}}
			>
				{#each weekDays as day (day.getTime())}
					{@const dayContent = getContentForDate(day)}
					{@const visibleContent = dayContent.slice(0, POSTS_PER_COLUMN)}
					{@const hiddenContent = dayContent.slice(POSTS_PER_COLUMN)}
					<div class="flex flex-col">
						<div class="mb-2 border-b pb-2 text-center">
							<WeeklyCalendarDayHeading date={new SvelteDate(day)} currentDate={new SvelteDate()} />
						</div>
						<div class="flex-1 space-y-3 overflow-hidden" style="height: {COLUMN_HEIGHT_WEEK}px;">
							{#each visibleContent as post (post.id)}
								<CalendarContentPreviewCardLarge
									{post}
									viewMode="week"
									onclick={() => onPostClick?.(post)}
								/>
							{/each}
							{#if hiddenContent.length > 0 && onOpenMore}
								<Button
									variant="outline"
									size="sm"
									class="w-full mt-2"
									onclick={() => onOpenMore(dayContent, day)}
								>
									({hiddenContent.length} More)
								</Button>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		{/key}
	</div>
{/if}
