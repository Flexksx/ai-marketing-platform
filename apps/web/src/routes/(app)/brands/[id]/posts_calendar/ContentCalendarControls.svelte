<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Calendar, ChevronLeft, ChevronRight } from '@lucide/svelte';
	import { SvelteDate } from 'svelte/reactivity';

	type CalendarViewMode = 'week' | 'month';

	type Props = {
		viewMode: CalendarViewMode;
		currentWeekStart: Date;
		currentMonthStart: Date;
		slideDirection: 'left' | 'right' | null;
	};

	let {
		viewMode = $bindable(),
		currentWeekStart = $bindable(),
		currentMonthStart = $bindable(),
		slideDirection = $bindable()
	}: Props = $props();

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

	const formatWeekRange = (startDate: Date): string => {
		const endDate = new SvelteDate(startDate);
		endDate.setDate(endDate.getDate() + 6);
		const startMonth = startDate.toLocaleDateString('en-US', { month: 'short' });
		const endMonth = endDate.toLocaleDateString('en-US', { month: 'short' });
		const startDay = startDate.getDate();
		const endDay = endDate.getDate();
		const year = startDate.getFullYear();

		if (startMonth === endMonth) {
			return `${startMonth} ${startDay} - ${endDay}, ${year}`;
		}
		return `${startMonth} ${startDay} - ${endMonth} ${endDay}, ${year}`;
	};

	const formatMonthYear = (date: Date): string => {
		return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
	};

	const displayTitle = $derived(
		viewMode === 'week' ? formatWeekRange(currentWeekStart) : formatMonthYear(currentMonthStart)
	);

	const goToPrevious = () => {
		if (viewMode === 'week') {
			slideDirection = 'right';
			const newDate = new SvelteDate(currentWeekStart);
			newDate.setDate(newDate.getDate() - 7);
			currentWeekStart = getStartOfWeek(newDate);
		} else {
			const newDate = new SvelteDate(currentMonthStart);
			newDate.setMonth(newDate.getMonth() - 1);
			currentMonthStart = getStartOfMonth(newDate);
		}
	};

	const goToNext = () => {
		if (viewMode === 'week') {
			slideDirection = 'left';
			const newDate = new SvelteDate(currentWeekStart);
			newDate.setDate(newDate.getDate() + 7);
			currentWeekStart = getStartOfWeek(newDate);
		} else {
			const newDate = new SvelteDate(currentMonthStart);
			newDate.setMonth(newDate.getMonth() + 1);
			currentMonthStart = getStartOfMonth(newDate);
		}
	};

	const goToCurrent = () => {
		if (viewMode === 'week') {
			slideDirection = null;
			currentWeekStart = getStartOfWeek();
		} else {
			currentMonthStart = getStartOfMonth();
		}
	};

	const toggleView = () => {
		if (viewMode === 'week') {
			viewMode = 'month';
			currentMonthStart = getStartOfMonth(currentWeekStart);
		} else {
			viewMode = 'week';
			slideDirection = null;
			currentWeekStart = getStartOfWeek(new SvelteDate());
		}
	};
</script>

<div class="mb-6 flex items-center justify-between flex-shrink-0">
	<div class="flex items-center space-x-4">
		<Button variant="outline" class="btn-rounded-full" size="sm" onclick={goToPrevious}>
			<ChevronLeft class="h-4 w-4" />
		</Button>
		<Button variant="outline" class="btn-rounded-full" size="sm" onclick={goToNext}>
			<ChevronRight class="h-4 w-4" />
		</Button>
		<div class="text-center">
			<h2 class="text-xl font-semibold">{displayTitle}</h2>
		</div>
	</div>
	<div class="flex items-center gap-2">
		<Button
			variant={viewMode === 'week' ? 'default' : 'outline'}
			size="sm"
			class="btn-rounded-full"
			onclick={toggleView}
		>
			<Calendar class="mr-2 h-4 w-4" />
			{viewMode === 'week' ? 'Week' : 'Month'}
		</Button>
		<Button variant="outline" size="sm" class="btn-rounded-full" onclick={goToCurrent}>Today</Button
		>
	</div>
</div>
