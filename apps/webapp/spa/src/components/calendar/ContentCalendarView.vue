<script setup lang="ts">
import { getBrandContent } from "@ai-marketing-platform/platform-api-client";
import { useQuery } from "@tanstack/vue-query";
import { computed } from "vue";
import { Badge } from "@/components/ui/badge";
import { useContentCalendarState } from "@/composables/useContentCalendarState";
import { asCalendarDate } from "@/lib/calendar/asCalendarDate";
import { groupScheduledContentByDay, placeContentInRange } from "@/lib/calendar/scheduledContent";
import CalendarToolbar from "./CalendarToolbar.vue";
import WeekViewCalendarPage from "./WeekViewCalendarPage.vue";
import MonthViewCalendarPage from "./MonthViewCalendarPage.vue";

const props = defineProps<{ brandId: string }>();

const locale = typeof navigator !== "undefined" ? navigator.language : "en-GB";

const {
	focused,
	view,
	viewRange,
	weekDays,
	periodLabel,
	setToday,
	goPrevious,
	goNext,
} = useContentCalendarState(locale);

const contentQ = useQuery({
	queryKey: computed(() => ["brands", props.brandId, "content"]),
	enabled: computed(() => !!props.brandId),
	queryFn: () => getBrandContent().search1(props.brandId),
});
const contentItems = computed(() => contentQ.data.value);

const inRange = computed(() => placeContentInRange(contentItems.value, viewRange.value));
const contentByDay = computed(() => groupScheduledContentByDay(inRange.value.scheduled));

const showNoContent = computed(
	() => !!props.brandId && !contentQ.isPending.value && (contentItems.value?.length ?? 0) === 0,
);
const showUnscheduled = computed(
	() => !!props.brandId
		&& inRange.value.unscheduled.length > 0
		&& (contentItems.value?.length ?? 0) > 0,
);

const monthGridAnchor = computed(() => asCalendarDate(focused.value));
</script>

<template>
	<section class="rounded-xl border border-border bg-card overflow-hidden w-full min-w-0">
		<div class="px-5 py-4 border-b border-border space-y-3">
			<h1 class="text-xl font-semibold tracking-tight">Calendar</h1>
			<CalendarToolbar
				v-model:view="view"
				:period-label="periodLabel"
				@today="setToday"
				@prev="goPrevious"
				@next="goNext"
			/>
		</div>

		<WeekViewCalendarPage
			v-if="view === 'week'"
			:locale="locale"
			:week-days="weekDays"
			:content-by-day="contentByDay"
		/>
		<MonthViewCalendarPage
			v-else
			:locale="locale"
			:month-anchor="monthGridAnchor"
			:content-by-day="contentByDay"
		/>

		<div v-if="showNoContent || showUnscheduled" class="px-5 py-4 border-t border-border">
			<p v-if="showNoContent" class="text-muted-foreground text-sm">
				No content for this brand yet. When items include
				<code class="bg-muted rounded px-1 text-xs">scheduledAt</code>
				they will show in the grid.
			</p>
			<template v-else-if="showUnscheduled">
				<p class="text-muted-foreground text-sm mb-2">
					Not on the calendar: items without
					<code class="bg-muted rounded px-1 text-xs">scheduledAt</code>.
				</p>
				<div class="flex flex-wrap gap-1.5">
					<Badge
						v-for="u in inRange.unscheduled"
						:key="u.id ?? 'unknown'"
						variant="secondary"
						:title="u.id"
					>
						{{ (u.id ?? "unknown").length > 20 ? `${(u.id ?? "…").slice(0, 8)}…` : u.id }}
					</Badge>
				</div>
			</template>
		</div>
	</section>
</template>
