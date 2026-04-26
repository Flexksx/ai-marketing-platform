import type { CalendarDate, DateValue } from "@internationalized/date";
import { toCalendarDate } from "@internationalized/date";

/**
 * Casts the date helpers from `@internationalized/date` to the concrete
 * `CalendarDate` class so Vue props / refs match the branded type the compiler
 * expects.
 */
export function asCalendarDate(d: unknown): CalendarDate {
	// `startOfWeek` et al. return a structural `CalendarDate` the compiler
	// will not pass to `toCalendarDate` without a cast.
	return toCalendarDate(d as DateValue) as CalendarDate;
}
