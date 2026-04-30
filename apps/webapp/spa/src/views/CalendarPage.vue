<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import ContentCalendarView from "@/components/calendar/ContentCalendarView.vue";

const route = useRoute();
const brandId = computed(() => route.params.brandId as string);
</script>

<template>
	<ContentCalendarView :brand-id="brandId" />
</template>
