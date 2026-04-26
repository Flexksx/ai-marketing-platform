import { getLocalTimeZone, fromDate } from "@internationalized/date";
import type { ContentItemResponse } from "@ai-marketing-platform/platform-api-client";
import { asCalendarDate } from "./asCalendarDate";
import type { DateRange, ScheduledContent } from "./types";
import { dayKey } from "./keys";

type ContentItemWithSchedule = ContentItemResponse & { scheduledAt?: string };

function displayLabelForContentId(id: string) {
	const t = id.trim();
	if (t.length <= 10) {
		return t;
	}
	return `${t.slice(0, 6)}…${t.slice(-4)}`;
}

/**
 * Splits brand `ContentItemResponse` into items that fall in `visible` with a
 * `scheduledAt` (from JSON, until OpenAPI exposes it) vs items without a schedule.
 */
export function placeContentInRange(
	items: ContentItemResponse[] | undefined,
	visible: DateRange,
): { scheduled: ScheduledContent[]; unscheduled: ContentItemResponse[] } {
	if (!items?.length) {
		return { scheduled: [], unscheduled: [] };
	}
	const tz = getLocalTimeZone();
	const scheduled: ScheduledContent[] = [];
	const unscheduled: ContentItemResponse[] = [];
	for (const item of items) {
		const raw = item as ContentItemWithSchedule;
		if (!raw.scheduledAt) {
			unscheduled.push(item);
			continue;
		}
		const t = new Date(raw.scheduledAt);
		if (Number.isNaN(t.getTime())) {
			unscheduled.push(item);
			continue;
		}
		const day = asCalendarDate(fromDate(t, tz));
		if (day.compare(visible.start) < 0 || day.compare(visible.end) > 0) {
			continue;
		}
		const id = item.id;
		if (!id) {
			continue;
		}
		scheduled.push({
			id,
			displayLabel: displayLabelForContentId(id),
			day,
		});
	}
	return { scheduled, unscheduled };
}

export function groupScheduledContentByDay(
	scheduled: ScheduledContent[],
): ReadonlyMap<string, ScheduledContent[]> {
	const map = new Map<string, ScheduledContent[]>();
	for (const c of scheduled) {
		const k = dayKey(c.day);
		const g = map.get(k);
		if (g) {
			g.push(c);
		} else {
			map.set(k, [c]);
		}
	}
	return map;
}
