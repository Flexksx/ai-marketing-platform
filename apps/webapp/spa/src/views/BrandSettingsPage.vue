<script setup lang="ts">
import { useRoute, RouterLink } from "vue-router";
import { computed } from "vue";
import { ChevronLeft } from "lucide-vue-next";
import BrandSettingsView from "@/components/brand/BrandSettingsView.vue";

const route = useRoute();
const brandId = computed(() => route.params.brandId as string);
</script>

<template>
	<div class="space-y-4">
		<RouterLink
			:to="{ name: 'brands' }"
			class="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
		>
			<ChevronLeft class="size-4" />
			All brands
		</RouterLink>
		<BrandSettingsView :brand-id="brandId" />
	</div>
</template>
