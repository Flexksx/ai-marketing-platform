<script setup lang="ts">
import { computed } from "vue";
import {
	getLocalTimeZone,
	isEqualMonth,
	isToday,
	type CalendarDate,
} from "@internationalized/date";
import { dayKey } from "@/lib/calendar/keys";
import { monthViewCells } from "@/lib/calendar/monthGrid";
import type { ScheduledContent } from "@/lib/calendar/types";
import { cn } from "@/lib/utils";
import ContentSchedulePill from "./ContentSchedulePill.vue";

const MAX_VISIBLE = 2;
const weekDayCount = 7;

const props = defineProps<{
	locale: string;
	monthAnchor: CalendarDate;
	contentByDay: ReadonlyMap<string, ScheduledContent[]>;
}>();

const zone = getLocalTimeZone();

const gridDays = computed(() => monthViewCells(props.monthAnchor, props.locale));
const weekHeaderLabels = computed(() => {
	const w = new Intl.DateTimeFormat(props.locale, { weekday: "short" });
	const d = gridDays.value[0];
	if (!d) {
		return [] as string[];
	}
	return Array.from({ length: weekDayCount }, (_, i) =>
		w.format(d.add({ days: i }).toDate(zone)),
	);
});
</script>

<template>
	<div
		class="border-border w-full min-w-0 overflow-hidden rounded-xl border"
	>
		<div class="overflow-x-auto">
			<div
				class="text-muted-foreground/90 border-border min-w-max border-b p-1 text-center text-xs font-medium"
			>
				<div
					class="grid w-full"
					:style="{ gridTemplateColumns: `repeat(${weekDayCount}, minmax(0, 1fr))` }"
				>
					<div
						v-for="(label, i) in weekHeaderLabels"
						:key="i"
						class="p-1"
					>
						{{ label }}
					</div>
				</div>
			</div>
			<div
				class="grid w-full min-w-max"
				:style="{ gridTemplateColumns: `repeat(${weekDayCount}, minmax(0, 1fr))` }"
			>
			<div
				v-for="(d, idx) in gridDays"
				:key="`d-${d.toString()}-${idx}`"
				data-slot="month-day-cell"
				:class="cn('border-border min-h-24 border-b border-r p-0.5', !isEqualMonth(d, monthAnchor) && 'bg-muted/15 opacity-50')"
			>
				<div
					:class="cn('mb-0.5 text-right text-xs', isToday(d, zone) && 'text-primary font-semibold', !isEqualMonth(d, monthAnchor) && 'text-muted-foreground/80', isEqualMonth(d, monthAnchor) && 'text-foreground/90')"
				>
					{{
						new Intl.DateTimeFormat(props.locale, { day: "numeric" }).format(
							d.toDate(zone),
						)
					}}
				</div>
				<div class="flex flex-col gap-0.5">
					<ContentSchedulePill
						v-for="c in (contentByDay.get(dayKey(d)) ?? []).slice(0, MAX_VISIBLE)"
						:key="c.id"
						:display-label="c.displayLabel"
					/>
					<span
						v-if="(contentByDay.get(dayKey(d)) ?? []).length > MAX_VISIBLE"
						class="text-muted-foreground px-0.5 text-left text-xs"
					>
						+{{
							(contentByDay.get(dayKey(d)) ?? []).length - MAX_VISIBLE
						}}
						more
					</span>
				</div>
			</div>
			</div>
		</div>
	</div>
</template>
