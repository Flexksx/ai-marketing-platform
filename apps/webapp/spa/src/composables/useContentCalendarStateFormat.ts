import { getLocalTimeZone, startOfWeek, type CalendarDate, type DateValue } from "@internationalized/date";
import { asCalendarDate } from "@/lib/calendar/asCalendarDate";
import type { DateRange, CalendarViewMode } from "@/lib/calendar/types";

const WEEK_DAYS = 7;

type WeekStart = "mon" | "tue" | "wed" | "thu" | "fri" | "sat" | "sun";

export function weekColumnDays(
	focused: CalendarDate,
	locale: string,
	weekStart: WeekStart,
) {
	const start = asCalendarDate(
		startOfWeek(focused as DateValue, locale, weekStart),
	);
	return Array.from({ length: WEEK_DAYS }, (_, i) => start.add({ days: i }));
}

/**
 * `weekRange` is the inclusive Monday–Sunday span for the focused week; used only for the week view label.
 */
export function formatViewPeriodLabel(
	focused: CalendarDate,
	weekRange: DateRange,
	mode: CalendarViewMode,
	locale: string,
): string {
	const tz = getLocalTimeZone();
	if (mode === "month") {
		return new Intl.DateTimeFormat(locale, {
			month: "long",
			year: "numeric",
		}).format(focused.toDate(tz));
	}
	const start = weekRange.start;
	const end = weekRange.end;
	const dtfDay = new Intl.DateTimeFormat(locale, { day: "numeric" });
	const dtfMon = new Intl.DateTimeFormat(locale, { month: "short" });
	const dtfYear = new Intl.DateTimeFormat(locale, { year: "numeric" });
	if (start.month === end.month && start.year === end.year) {
		return `${dtfDay.format(start.toDate(tz))}–${dtfDay.format(end.toDate(tz))} ${dtfMon.format(
			start.toDate(tz),
		)} ${dtfYear.format(start.toDate(tz))}`;
	}
	return `${dtfDay.format(start.toDate(tz))} ${dtfMon.format(start.toDate(tz))} – ${dtfDay.format(
		end.toDate(tz),
	)} ${dtfMon.format(end.toDate(tz))} ${dtfYear.format(end.toDate(tz))}`;
}
