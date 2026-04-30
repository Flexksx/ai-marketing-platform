<script setup lang="ts">
import { Trash2, X, Plus } from "lucide-vue-next";
import type { AudienceFormItem } from "@/lib/brands/useBrandSettingsForm";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";

const props = defineProps<{
	audiences: AudienceFormItem[];
	isLoading: boolean;
}>();

const FUNNEL_STAGES = [
	{ value: "TOFU", label: "Top of funnel" },
	{ value: "MOFU", label: "Middle of funnel" },
	{ value: "BOFU", label: "Bottom of funnel" },
] as const;

const addAudience = () => {
	props.audiences.push({ name: "", funnel_stage: "", desires: [], pain_points: [] });
};

const removeAudience = (index: number) => {
	props.audiences.splice(index, 1);
};

const addStringItem = (list: string[]) => {
	list.push("");
};

const removeStringItem = (list: string[], index: number) => {
	list.splice(index, 1);
};
</script>

<template>
	<section class="rounded-xl border border-border bg-card overflow-hidden">
		<div class="px-5 py-4 border-b border-border flex items-start justify-between gap-3">
			<div>
				<h2 class="text-sm font-semibold tracking-tight">Target Audiences</h2>
				<p class="text-xs text-muted-foreground mt-0.5">Audience segments grouped by funnel stage.</p>
			</div>
		</div>

		<div class="px-5 py-4 space-y-3">
			<template v-if="isLoading">
				<Skeleton class="h-24 w-full" />
				<Skeleton class="h-24 w-full" />
			</template>

			<template v-else>
				<div
					v-for="(audience, audienceIndex) in audiences"
					:key="audienceIndex"
					class="rounded-lg border border-border bg-background/60 p-4 space-y-4"
				>
					<div class="flex items-start gap-2">
						<div class="grid gap-1.5 flex-1">
							<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Name</label>
							<Input v-model="audience.name" placeholder="Audience name" />
						</div>
						<div class="grid gap-1.5 w-44 shrink-0">
							<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Funnel Stage</label>
							<Select v-model="audience.funnel_stage">
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
							@click="removeAudience(audienceIndex)"
						>
							<Trash2 class="size-4" />
						</button>
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Desires</label>
						<div class="space-y-1.5">
							<div v-for="(_, desireIndex) in audience.desires" :key="desireIndex" class="flex gap-1.5">
								<Input v-model="audience.desires[desireIndex]" placeholder="What this audience desires…" class="flex-1" />
								<button
									type="button"
									class="shrink-0 rounded-md p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/8 transition-colors cursor-pointer"
									@click="removeStringItem(audience.desires, desireIndex)"
								>
									<X class="size-4" />
								</button>
							</div>
							<button
								type="button"
								class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-primary transition-colors px-1 py-0.5 cursor-pointer"
								@click="addStringItem(audience.desires)"
							>
								<Plus class="size-3.5" />
								Add desire
							</button>
						</div>
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Pain Points</label>
						<div class="space-y-1.5">
							<div v-for="(_, pointIndex) in audience.pain_points" :key="pointIndex" class="flex gap-1.5">
								<Input v-model="audience.pain_points[pointIndex]" placeholder="A pain point…" class="flex-1" />
								<button
									type="button"
									class="shrink-0 rounded-md p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/8 transition-colors cursor-pointer"
									@click="removeStringItem(audience.pain_points, pointIndex)"
								>
									<X class="size-4" />
								</button>
							</div>
							<button
								type="button"
								class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-primary transition-colors px-1 py-0.5 cursor-pointer"
								@click="addStringItem(audience.pain_points)"
							>
								<Plus class="size-3.5" />
								Add pain point
							</button>
						</div>
					</div>
				</div>

				<button
					type="button"
					class="flex w-full cursor-pointer items-center justify-center gap-1.5 rounded-lg border border-dashed border-border py-2.5 text-xs text-muted-foreground transition-colors hover:border-primary/40 hover:text-primary hover:bg-primary/4"
					@click="addAudience"
				>
					<Plus class="size-3.5" />
					Add audience
				</button>
			</template>
		</div>
	</section>
</template>
