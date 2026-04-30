<script setup lang="ts">
import { Trash2, X, Plus } from "lucide-vue-next";
import type { PillarFormItem } from "@/lib/brands/useBrandSettingsForm";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";

const props = defineProps<{
	pillars: PillarFormItem[];
	isLoading: boolean;
}>();

const FUNNEL_STAGES = [
	{ value: "TOFU", label: "Top of funnel" },
	{ value: "MOFU", label: "Middle of funnel" },
	{ value: "BOFU", label: "Bottom of funnel" },
] as const;

const addPillar = () => {
	props.pillars.push({ name: "", topic: "", funnel_stage: "", content_type_indicators: [] });
};

const removePillar = (index: number) => {
	props.pillars.splice(index, 1);
};

const addIndicator = (list: string[]) => {
	list.push("");
};

const removeIndicator = (list: string[], index: number) => {
	list.splice(index, 1);
};
</script>

<template>
	<section class="rounded-xl border border-border bg-card overflow-hidden">
		<div class="px-5 py-4 border-b border-border">
			<h2 class="text-sm font-semibold tracking-tight">Content Pillars</h2>
			<p class="text-xs text-muted-foreground mt-0.5">Content strategy pillars mapped to funnel stages.</p>
		</div>

		<div class="px-5 py-4 space-y-3">
			<template v-if="isLoading">
				<Skeleton class="h-24 w-full" />
				<Skeleton class="h-24 w-full" />
			</template>

			<template v-else>
				<div
					v-for="(pillar, pillarIndex) in pillars"
					:key="pillarIndex"
					class="rounded-lg border border-border bg-background/60 p-4 space-y-4"
				>
					<div class="flex items-start gap-2">
						<div class="grid gap-1.5 flex-1">
							<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Name</label>
							<Input v-model="pillar.name" placeholder="Pillar name" />
						</div>
						<div class="grid gap-1.5 w-44 shrink-0">
							<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Funnel Stage</label>
							<Select v-model="pillar.funnel_stage">
								<SelectTrigger class="h-8">
									<SelectValue placeholder="Stage" />
								</SelectTrigger>
								<SelectContent>
									<SelectItem v-for="stage in FUNNEL_STAGES" :key="stage.value" :value="stage.value">
										{{ stage.label }}
									</SelectItem>
								</SelectContent>
							</Select>
						</div>
						<button
							type="button"
							class="mt-5 shrink-0 rounded-md p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/8 transition-colors cursor-pointer"
							@click="removePillar(pillarIndex)"
						>
							<Trash2 class="size-4" />
						</button>
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Topic</label>
						<Textarea v-model="pillar.topic" placeholder="Topic or description of the content needed…" class="resize-none" rows="2" />
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Content Types</label>
						<div class="space-y-1.5">
							<div v-for="(_, indicatorIndex) in pillar.content_type_indicators" :key="indicatorIndex" class="flex gap-1.5">
								<Input
									v-model="pillar.content_type_indicators[indicatorIndex]"
									placeholder="e.g. blog post, video, infographic…"
									class="flex-1"
								/>
								<button
									type="button"
									class="shrink-0 rounded-md p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/8 transition-colors cursor-pointer"
									@click="removeIndicator(pillar.content_type_indicators, indicatorIndex)"
								>
									<X class="size-4" />
								</button>
							</div>
							<button
								type="button"
								class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-primary transition-colors px-1 py-0.5 cursor-pointer"
								@click="addIndicator(pillar.content_type_indicators)"
							>
								<Plus class="size-3.5" />
								Add content type
							</button>
						</div>
					</div>
				</div>

				<button
					type="button"
					class="flex w-full cursor-pointer items-center justify-center gap-1.5 rounded-lg border border-dashed border-border py-2.5 text-xs text-muted-foreground transition-colors hover:border-primary/40 hover:text-primary hover:bg-primary/4"
					@click="addPillar"
				>
					<Plus class="size-3.5" />
					Add pillar
				</button>
			</template>
		</div>
	</section>
</template>
