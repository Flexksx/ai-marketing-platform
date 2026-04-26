import { startOfMonth, startOfWeek, type CalendarDate } from "@internationalized/date";
import { asCalendarDate } from "./asCalendarDate";

const WEEK_DAYS = 7;
const WEEKS_IN_VIEW = 6;
const GRID = WEEK_DAYS * WEEKS_IN_VIEW;

/** Six-week grid starting the Monday of the week that contains the first of the month. */
export function monthViewCells(anchor: CalendarDate, locale: string): CalendarDate[] {
	const m0 = asCalendarDate(startOfMonth(anchor));
	const grid0 = asCalendarDate(startOfWeek(m0, locale, "mon"));
	return Array.from({ length: GRID }, (_, i) => grid0.add({ days: i }));
}
