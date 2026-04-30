<script setup lang="ts">
import { useRoute, RouterLink } from "vue-router";
import { computed } from "vue";
import BrandSettingsView from "@/components/brand/BrandSettingsView.vue";

const route = useRoute();
const brandId = computed(() => route.params.brandId as string);
</script>

<template>
	<div class="space-y-4">
		<RouterLink
			:to="{ name: 'brands' }"
			class="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
		>
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-3.5">
				<path fill-rule="evenodd" d="M9.78 4.22a.75.75 0 0 1 0 1.06L7.06 8l2.72 2.72a.75.75 0 1 1-1.06 1.06L5.47 8.53a.75.75 0 0 1 0-1.06l3.25-3.25a.75.75 0 0 1 1.06 0Z" clip-rule="evenodd" />
			</svg>
			All brands
		</RouterLink>
		<BrandSettingsView :brand-id="brandId" />
	</div>
</template>
