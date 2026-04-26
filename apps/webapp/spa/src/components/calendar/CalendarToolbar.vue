<script setup lang="ts">
import { ChevronLeft, ChevronRight } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import type { CalendarViewMode } from "@/lib/calendar/types";

const view = defineModel<CalendarViewMode>("view", { required: true });

const props = defineProps<{
	periodLabel: string;
}>();
const emit = defineEmits<{
	prev: [];
	next: [];
	today: [];
}>();
</script>

<template>
	<div class="border-border flex flex-col gap-2 border-b pb-3 sm:flex-row sm:items-center sm:justify-between sm:pb-0 sm:border-0 sm:pt-0">
		<div class="text-foreground/90 min-w-0 text-base font-medium tracking-tight">
			{{ props.periodLabel }}
		</div>
		<div class="flex flex-wrap items-center gap-2 sm:gap-1">
			<ToggleGroup
				v-model="view"
				aria-label="Calendar view"
				variant="outline"
				:spacing="0"
				type="single"
			>
				<ToggleGroupItem value="week" aria-label="Week view" class="text-xs sm:text-sm">
					Week
				</ToggleGroupItem>
				<ToggleGroupItem value="month" aria-label="Month view" class="text-xs sm:text-sm">
					Month
				</ToggleGroupItem>
			</ToggleGroup>
			<Button
				aria-label="Go to today"
				class="h-8 text-xs sm:text-sm"
				size="sm"
				variant="outline"
				@click="emit('today')"
			>
				Today
			</Button>
			<div class="ml-auto flex items-center sm:ml-0">
				<Button
					aria-label="Previous period"
					size="icon-sm"
					variant="outline"
					@click="emit('prev')"
				>
					<ChevronLeft :size="18" class="shrink-0" />
				</Button>
				<Button
					aria-label="Next period"
					size="icon-sm"
					variant="outline"
					@click="emit('next')"
				>
					<ChevronRight :size="18" class="shrink-0" />
				</Button>
			</div>
		</div>
	</div>
</template>
