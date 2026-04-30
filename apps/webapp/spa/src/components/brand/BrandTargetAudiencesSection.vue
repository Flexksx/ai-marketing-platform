<script setup lang="ts">
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
									<SelectItem
										v-for="stage in FUNNEL_STAGES"
										:key="stage.value"
										:value="stage.value"
									>
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
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4">
								<path fill-rule="evenodd" d="M5 3.25V4H2.75a.75.75 0 0 0 0 1.5h.3l.815 8.15A1.5 1.5 0 0 0 5.357 15h5.285a1.5 1.5 0 0 0 1.493-1.35l.815-8.15h.3a.75.75 0 0 0 0-1.5H11v-.75A2.25 2.25 0 0 0 8.75 1h-1.5A2.25 2.25 0 0 0 5 3.25Zm2.25-.75a.75.75 0 0 0-.75.75V4h3v-.75a.75.75 0 0 0-.75-.75h-1.5ZM6.05 6a.75.75 0 0 1 .787.713l.275 5.5a.75.75 0 0 1-1.498.075l-.275-5.5A.75.75 0 0 1 6.05 6Zm3.9 0a.75.75 0 0 1 .712.787l-.275 5.5a.75.75 0 0 1-1.498-.075l.275-5.5a.75.75 0 0 1 .786-.711Z" clip-rule="evenodd" />
							</svg>
						</button>
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Desires</label>
						<div class="space-y-1.5">
							<div
								v-for="(_, desireIndex) in audience.desires"
								:key="desireIndex"
								class="flex gap-1.5"
							>
								<Input
									v-model="audience.desires[desireIndex]"
									placeholder="What this audience desires…"
									class="flex-1"
								/>
								<button
									type="button"
									class="shrink-0 rounded-md p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/8 transition-colors cursor-pointer"
									@click="removeStringItem(audience.desires, desireIndex)"
								>
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4">
										<path d="M5.28 4.22a.75.75 0 0 0-1.06 1.06L6.94 8l-2.72 2.72a.75.75 0 1 0 1.06 1.06L8 9.06l2.72 2.72a.75.75 0 1 0 1.06-1.06L9.06 8l2.72-2.72a.75.75 0 0 0-1.06-1.06L8 6.94 5.28 4.22Z" />
									</svg>
								</button>
							</div>
							<button
								type="button"
								class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-primary transition-colors px-1 py-0.5 cursor-pointer"
								@click="addStringItem(audience.desires)"
							>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-3.5">
									<path d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z" />
								</svg>
								Add desire
							</button>
						</div>
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Pain Points</label>
						<div class="space-y-1.5">
							<div
								v-for="(_, pointIndex) in audience.pain_points"
								:key="pointIndex"
								class="flex gap-1.5"
							>
								<Input
									v-model="audience.pain_points[pointIndex]"
									placeholder="A pain point…"
									class="flex-1"
								/>
								<button
									type="button"
									class="shrink-0 rounded-md p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/8 transition-colors cursor-pointer"
									@click="removeStringItem(audience.pain_points, pointIndex)"
								>
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4">
										<path d="M5.28 4.22a.75.75 0 0 0-1.06 1.06L6.94 8l-2.72 2.72a.75.75 0 1 0 1.06 1.06L8 9.06l2.72 2.72a.75.75 0 1 0 1.06-1.06L9.06 8l2.72-2.72a.75.75 0 0 0-1.06-1.06L8 6.94 5.28 4.22Z" />
									</svg>
								</button>
							</div>
							<button
								type="button"
								class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-primary transition-colors px-1 py-0.5 cursor-pointer"
								@click="addStringItem(audience.pain_points)"
							>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-3.5">
									<path d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z" />
								</svg>
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
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-3.5">
						<path d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z" />
					</svg>
					Add audience
				</button>
			</template>
		</div>
	</section>
</template>
