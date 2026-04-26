import {
	endOfMonth,
	endOfWeek,
	getLocalTimeZone,
	startOfMonth,
	startOfWeek,
	today,
} from "@internationalized/date";
import { computed, ref, type ComputedRef, type Ref } from "vue";
import type { CalendarDate, DateValue } from "@internationalized/date";
import type { CalendarViewMode, DateRange } from "@/lib/calendar/types";
import { asCalendarDate } from "@/lib/calendar/asCalendarDate";
import { formatViewPeriodLabel, weekColumnDays } from "@/composables/useContentCalendarStateFormat";

const WEEK_START = "mon" as const;

export function useContentCalendarState(locale: string) {
	const focused = ref<CalendarDate>(asCalendarDate(today(getLocalTimeZone())));
	const view: Ref<CalendarViewMode> = ref("week");

	const viewRange: ComputedRef<DateRange> = computed(() => {
		if (view.value === "week") {
			return {
				start: asCalendarDate(
					startOfWeek(focused.value as DateValue, locale, WEEK_START),
				),
				end: asCalendarDate(
					endOfWeek(focused.value as DateValue, locale, WEEK_START),
				),
			};
		}
		return {
			start: asCalendarDate(startOfMonth(focused.value as DateValue)),
			end: asCalendarDate(endOfMonth(focused.value as DateValue)),
		};
	});

	const weekDays = computed(() =>
		weekColumnDays(asCalendarDate(focused.value), locale, WEEK_START),
	);

	const periodLabel = computed(() =>
		formatViewPeriodLabel(
			asCalendarDate(focused.value),
			viewRange.value,
			view.value,
			locale,
		),
	);

	function setToday() {
		focused.value = asCalendarDate(today(getLocalTimeZone()));
	}

	function goPrevious() {
		const cur = asCalendarDate(focused.value);
		if (view.value === "week") {
			focused.value = asCalendarDate(cur.subtract({ weeks: 1 }));
		} else {
			focused.value = asCalendarDate(cur.subtract({ months: 1 }));
		}
	}

	function goNext() {
		const cur = asCalendarDate(focused.value);
		if (view.value === "week") {
			focused.value = asCalendarDate(cur.add({ weeks: 1 }));
		} else {
			focused.value = asCalendarDate(cur.add({ months: 1 }));
		}
	}

	return {
		focused,
		view,
		viewRange,
		weekDays,
		periodLabel,
		setToday,
		goPrevious,
		goNext,
	};
}
