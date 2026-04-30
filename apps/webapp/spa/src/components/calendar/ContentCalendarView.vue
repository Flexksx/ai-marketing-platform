<script setup lang="ts">
import { getBrands, getBrandContent } from "@ai-marketing-platform/platform-api-client";
import { useQuery } from "@tanstack/vue-query";
import { computed, ref, watch, type Ref } from "vue";
import { Badge } from "@/components/ui/badge";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import { useContentCalendarState } from "@/composables/useContentCalendarState";
import { asCalendarDate } from "@/lib/calendar/asCalendarDate";
import { groupScheduledContentByDay, placeContentInRange } from "@/lib/calendar/scheduledContent";
import CalendarToolbar from "./CalendarToolbar.vue";
import WeekViewCalendarPage from "./WeekViewCalendarPage.vue";
import MonthViewCalendarPage from "./MonthViewCalendarPage.vue";

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

const selectedBrandId: Ref<string | undefined> = ref();

const brandsQ = useQuery({
	queryKey: ["brands"],
	queryFn: () => getBrands().search(),
});
const brandList = computed(() => brandsQ.data.value);

watch(
	brandList,
	(b) => {
		if (!b?.length || selectedBrandId.value) {
			return;
		}
		selectedBrandId.value = b[0].id;
	},
	{ immediate: true },
);

const contentQ = useQuery({
	queryKey: ["brands", () => selectedBrandId.value, "content"] as const,
	enabled: () => !!selectedBrandId.value,
	queryFn: () => {
		const id = selectedBrandId.value;
		if (!id) {
			throw new Error("missing brandId");
		}
		return getBrandContent().search1(id);
	},
});
const contentItems = computed(() => contentQ.data.value);

const inRange = computed(() =>
	placeContentInRange(contentItems.value, viewRange.value),
);
const contentByDay = computed(() =>
	groupScheduledContentByDay(inRange.value.scheduled),
);

const showNoContent = computed(
	() =>
		!!selectedBrandId.value
		&& !contentQ.isPending.value
		&& (contentItems.value?.length ?? 0) === 0,
);
const showUnscheduled = computed(
	() => !!selectedBrandId.value
		&& inRange.value.unscheduled.length > 0
		&& (contentItems.value?.length ?? 0) > 0
);

const monthGridAnchor = computed(() => asCalendarDate(focused.value));
</script>

<template>
	<section class="rounded-xl border border-border bg-card overflow-hidden w-full min-w-0">
		<!-- Header -->
		<div class="px-5 py-4 border-b border-border space-y-3">
			<div class="flex w-full min-w-0 flex-col items-start justify-between gap-2 sm:flex-row sm:items-center sm:gap-3">
				<h1 class="text-xl font-semibold tracking-tight shrink-0">Content calendar</h1>
				<Select v-model="selectedBrandId">
					<SelectTrigger class="h-8 w-full min-w-[12rem] sm:max-w-xs" size="sm" aria-label="Active brand">
						<SelectValue
							:placeholder="brandsQ.isPending ? 'Loading brands…' : 'Choose brand'"
						/>
					</SelectTrigger>
					<SelectContent>
						<SelectItem
							v-for="b in (brandList ?? [])"
							:key="b.id"
							:value="b.id ?? 'unknown-brand'"
						>
							{{ b.name }}
						</SelectItem>
					</SelectContent>
				</Select>
			</div>
			<CalendarToolbar
				v-model:view="view"
				:period-label="periodLabel"
				@today="setToday"
				@prev="goPrevious"
				@next="goNext"
			/>
		</div>

		<!-- Calendar grid -->
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

		<!-- Footer: no content / unscheduled -->
		<div v-if="showNoContent || showUnscheduled" class="px-5 py-4 border-t border-border">
			<p
				v-if="showNoContent"
				class="text-muted-foreground text-sm"
			>
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
