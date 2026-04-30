<script setup lang="ts">
import type { BrandFormState } from "@/lib/brands/useBrandSettingsForm";
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
	CardDescription,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";

const props = defineProps<{
	form: BrandFormState;
	isLoading: boolean;
}>();
</script>

<template>
	<Card>
		<CardHeader>
			<CardTitle>General</CardTitle>
			<CardDescription>Basic brand information.</CardDescription>
		</CardHeader>
		<CardContent class="space-y-4">
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
					<Textarea v-model="form.description" placeholder="Describe the brand…" />
				</div>
			</template>
		</CardContent>
	</Card>
</template>
