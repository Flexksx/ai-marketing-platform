import type { CalendarDate } from "@internationalized/date";

export type CalendarViewMode = "week" | "month";

export interface DateRange {
	start: CalendarDate;
	end: CalendarDate;
}

/** One content item placed on a calendar day (in-range) for the grid. */
export interface ScheduledContent {
	id: string;
	/** Truncated id for display when there is no title in the API yet. */
	displayLabel: string;
	day: CalendarDate;
}
