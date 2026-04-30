<script setup lang="ts">
import type { BrandFormState } from "@/lib/brands/useBrandSettingsForm";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";

const props = defineProps<{
	form: BrandFormState;
	isLoading: boolean;
}>();
</script>

<template>
	<section class="rounded-xl border border-border bg-card overflow-hidden">
		<div class="px-5 py-4 border-b border-border">
			<h2 class="text-sm font-semibold tracking-tight">General</h2>
			<p class="text-xs text-muted-foreground mt-0.5">Basic brand information.</p>
		</div>
		<div class="px-5 py-4 space-y-4">
			<template v-if="isLoading">
				<Skeleton class="h-8 w-full" />
				<Skeleton class="h-8 w-full" />
				<Skeleton class="h-20 w-full" />
			</template>
			<template v-else>
				<div class="grid gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Name</label>
					<Input v-model="form.name" placeholder="Brand name" />
				</div>
				<div class="grid gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Website</label>
					<Input v-model="form.website_url" placeholder="https://example.com" type="url" />
				</div>
				<div class="grid gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Description</label>
					<Textarea v-model="form.description" placeholder="Describe the brand…" class="resize-none" rows="3" />
				</div>
			</template>
		</div>
	</section>
</template>
