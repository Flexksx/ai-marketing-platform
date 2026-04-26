<script setup lang="ts">
import type { HTMLAttributes } from "vue";
import { cn } from "@/lib/utils";

const props = defineProps<{
	displayLabel: string;
	class?: HTMLAttributes["class"];
}>();
</script>

<template>
	<div
		data-slot="content-schedule-pill"
		:class="
			cn(
				'bg-primary/8 text-foreground/90 truncate rounded border border-primary/20 px-1.5 py-0.5 text-left text-xs font-medium leading-tight',
				props.class,
			)
		"
		:title="displayLabel"
	>
		{{ displayLabel }}
	</div>
</template>
