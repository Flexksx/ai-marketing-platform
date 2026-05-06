<script lang="ts">
	import type { BrandAudience } from '$lib/api/brand-data/model/BrandData';
	import type { ContentPillarParsed } from '$lib/api/brand-data/schema/ContentPillar';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import {
		BookOpen,
		Clapperboard,
		Film,
		Layers,
		Lightbulb,
		Pencil,
		RefreshCw,
		ShoppingBag,
		Star,
		Target,
		TrendingUp,
		UserCheck,
		Users,
		Zap
	} from 'lucide-svelte';

	interface Props {
		pillar: ContentPillarParsed;
		audiences: BrandAudience[];
		readonly?: boolean;
		onEditRequested?: () => void;
	}

	let { pillar, audiences, readonly = false, onEditRequested }: Props = $props();

	const linkedAudienceNames = $derived(
		pillar.audienceIds
			.map((id) => audiences.find((a) => a.id === id)?.name)
			.filter((name): name is string => !!name)
	);

	const BUSINESS_GOAL_ICONS: Record<string, typeof Zap> = {
		DRIVE_ENGAGEMENT: Zap,
		INCREASE_CONVERSION: TrendingUp,
		BUILD_TRUST: UserCheck,
		GENERATE_LEADS: Target,
		RETENTION: RefreshCw
	};

	const PILLAR_TYPE_ICONS: Record<string, typeof Zap> = {
		EDUCATION: BookOpen,
		PRODUCT_SERVICE: ShoppingBag,
		SOCIAL_PROOF: Star,
		BEHIND_THE_SCENES: Clapperboard,
		ENTERTAINMENT: Film,
		COMMUNITY: Users,
		THOUGHT_LEADERSHIP: Lightbulb
	};

	function formatEnumLabel(value: string): string {
		return value
			.split('_')
			.map((w) => w.charAt(0) + w.slice(1).toLowerCase())
			.join(' ');
	}
</script>

<Card
	class="border bg-card/60 backdrop-blur-sm hover:bg-card transition-colors cursor-pointer rounded-3xl"
	onclick={() => {
		if (readonly || !onEditRequested) return;
		onEditRequested();
	}}
>
	<CardHeader class="flex flex-row items-start justify-between gap-4 px-4 pt-4 ">
		<CardTitle class="text-sm font-semibold break-words min-w-0">
			{pillar.name || 'Untitled pillar'}
		</CardTitle>
		{#if !readonly && onEditRequested}
			<Button
				type="button"
				size="icon"
				variant="ghost"
				class="h-7 w-7 shrink-0 -mt-0.5"
				onclick={(event) => {
					event.stopPropagation();
					onEditRequested();
				}}
			>
				<Pencil class="h-3 w-3" />
			</Button>
		{/if}
	</CardHeader>
	<CardContent class="space-y-2 px-4 pb-4 pt-0">
		<div class="flex flex-wrap gap-1.5">
			{#if BUSINESS_GOAL_ICONS[pillar.businessGoal]}
				{@const GoalIcon = BUSINESS_GOAL_ICONS[pillar.businessGoal]}
				<span
					class="inline-flex items-center gap-1 rounded-full bg-orange-100 px-2 py-0.5 text-[10px] font-medium text-orange-700 dark:bg-orange-900/30 dark:text-orange-300"
				>
					<GoalIcon class="h-2.5 w-2.5 shrink-0" />
					{formatEnumLabel(pillar.businessGoal)}
				</span>
			{/if}
			{#if PILLAR_TYPE_ICONS[pillar.type]}
				{@const TypeIcon = PILLAR_TYPE_ICONS[pillar.type]}
				<span
					class="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
				>
					<TypeIcon class="h-2.5 w-2.5 shrink-0" />
					{formatEnumLabel(pillar.type)}
				</span>
			{/if}
		</div>

		{#if pillar.contentTypes.length > 0}
			<div class="flex flex-wrap gap-1">
				{#each pillar.contentTypes as contentType (contentType)}
					<span
						class="inline-flex items-center gap-1 rounded-full bg-muted px-2 py-0.5 text-[10px] text-muted-foreground"
					>
						<Layers class="h-2.5 w-2.5 shrink-0" />
						{formatEnumLabel(contentType)}
					</span>
				{/each}
			</div>
		{/if}

		{#if linkedAudienceNames.length > 0}
			<div class="flex flex-wrap gap-1">
				{#each linkedAudienceNames as name (name)}
					<span
						class="inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[10px] text-muted-foreground"
					>
						<Users class="h-2.5 w-2.5 shrink-0" />
						{name}
					</span>
				{/each}
			</div>
		{/if}
	</CardContent>
</Card>
