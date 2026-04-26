import type { CalendarDate } from "@internationalized/date";

function pad2(n: number) {
	return String(n).padStart(2, "0");
}

/** Stable key for grouping by calendar day. */
export function dayKey(d: CalendarDate) {
	return `${d.year}-${pad2(d.month)}-${pad2(d.day)}`;
}
