<script setup lang="ts">
import { isToday, getLocalTimeZone, type CalendarDate } from "@internationalized/date";
import { dayKey } from "@/lib/calendar/keys";
import type { ScheduledContent } from "@/lib/calendar/types";
import { cn } from "@/lib/utils";
import ContentSchedulePill from "./ContentSchedulePill.vue";

const props = defineProps<{
	locale: string;
	weekDays: readonly CalendarDate[];
	contentByDay: ReadonlyMap<string, ScheduledContent[]>;
}>();

const zone = getLocalTimeZone();

function isTodayCell(d: CalendarDate) {
	return isToday(d, zone);
}
</script>

<template>
	<div class="border-border w-full min-w-0 overflow-x-auto">
		<div
			class="grid w-full"
			:style="{ gridTemplateColumns: `repeat(${Math.max(weekDays.length, 1)}, minmax(6rem, 1fr))` }"
		>
			<div
				v-for="d in props.weekDays"
				:key="d.toString()"
				class="border-border bg-muted/25 text-muted-foreground/90 border-b border-r p-1.5 text-center text-xs font-medium last:border-r-0"
			>
				<div
					:class="cn('flex min-h-10 flex-col justify-center', isTodayCell(d) && 'text-primary')">
					{{
						new Intl.DateTimeFormat(props.locale, { weekday: "short" }).format(d.toDate(zone))
					}}
				</div>
				<div
					:class="cn('text-foreground/80 text-sm font-medium', isTodayCell(d) && 'text-primary')"
				>
					{{
						new Intl.DateTimeFormat(props.locale, { day: "numeric" }).format(d.toDate(zone))
					}}
				</div>
			</div>
			<div
				v-for="d in props.weekDays"
				:key="`b-${d.toString()}`"
				class="border-border bg-card min-h-36 border-b border-r p-1 last:border-r-0"
			>
				<div class="flex h-full min-h-32 flex-col gap-0.5 overflow-y-auto">
					<ContentSchedulePill
						v-for="c in (contentByDay.get(dayKey(d)) ?? [])"
						:key="c.id"
						:display-label="c.displayLabel"
					/>
					<template
						v-if="!contentByDay.get(dayKey(d))?.length"
					>
						<span
							class="text-muted-foreground/70 mt-1 w-full p-0.5 text-center text-xs"
						>
							—
						</span>
					</template>
				</div>
			</div>
		</div>
	</div>
</template>
