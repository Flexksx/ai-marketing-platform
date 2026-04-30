<script setup lang="ts">
import type { PillarFormItem } from "@/lib/brands/useBrandSettingsForm";
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
	CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
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
	<Card>
		<CardHeader>
			<CardTitle>Content Pillars</CardTitle>
			<CardDescription>Content strategy pillars mapped to funnel stages.</CardDescription>
		</CardHeader>
		<CardContent class="space-y-4">
			<template v-if="isLoading">
				<Skeleton class="h-20 w-full" />
				<Skeleton class="h-20 w-full" />
			</template>

			<template v-else>
				<div
					v-for="(pillar, pillarIndex) in pillars"
					:key="pillarIndex"
					class="rounded-lg border border-border p-4 space-y-4"
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
						<Button
							variant="ghost"
							size="icon-sm"
							class="mt-5 shrink-0 text-muted-foreground hover:text-destructive"
							type="button"
							@click="removePillar(pillarIndex)"
						>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4">
								<path fill-rule="evenodd" d="M5 3.25V4H2.75a.75.75 0 0 0 0 1.5h.3l.815 8.15A1.5 1.5 0 0 0 5.357 15h5.285a1.5 1.5 0 0 0 1.493-1.35l.815-8.15h.3a.75.75 0 0 0 0-1.5H11v-.75A2.25 2.25 0 0 0 8.75 1h-1.5A2.25 2.25 0 0 0 5 3.25Zm2.25-.75a.75.75 0 0 0-.75.75V4h3v-.75a.75.75 0 0 0-.75-.75h-1.5ZM6.05 6a.75.75 0 0 1 .787.713l.275 5.5a.75.75 0 0 1-1.498.075l-.275-5.5A.75.75 0 0 1 6.05 6Zm3.9 0a.75.75 0 0 1 .712.787l-.275 5.5a.75.75 0 0 1-1.498-.075l.275-5.5a.75.75 0 0 1 .786-.711Z" clip-rule="evenodd" />
							</svg>
						</Button>
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Topic</label>
						<Textarea v-model="pillar.topic" placeholder="Topic or description of the content needed…" />
					</div>

					<div class="grid gap-1.5">
						<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide">Content Types</label>
						<div class="space-y-1.5">
							<div
								v-for="(_, indicatorIndex) in pillar.content_type_indicators"
								:key="indicatorIndex"
								class="flex gap-1.5"
							>
								<Input
									v-model="pillar.content_type_indicators[indicatorIndex]"
									placeholder="e.g. blog post, video, infographic…"
									class="flex-1"
								/>
								<Button
									variant="ghost"
									size="icon-sm"
									type="button"
									class="shrink-0 text-muted-foreground hover:text-destructive"
									@click="removeIndicator(pillar.content_type_indicators, indicatorIndex)"
								>
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4">
										<path d="M5.28 4.22a.75.75 0 0 0-1.06 1.06L6.94 8l-2.72 2.72a.75.75 0 1 0 1.06 1.06L8 9.06l2.72 2.72a.75.75 0 1 0 1.06-1.06L9.06 8l2.72-2.72a.75.75 0 0 0-1.06-1.06L8 6.94 5.28 4.22Z" />
									</svg>
								</Button>
							</div>
							<Button
								variant="ghost"
								size="sm"
								type="button"
								class="text-muted-foreground h-7 px-2"
								@click="addIndicator(pillar.content_type_indicators)"
							>
								+ Add content type
							</Button>
						</div>
					</div>
				</div>

				<Button
					variant="outline"
					size="sm"
					type="button"
					class="w-full"
					@click="addPillar"
				>
					+ Add pillar
				</Button>
			</template>
		</CardContent>
	</Card>
</template>
