<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import { Calendar, Users, Sparkles, Loader2 } from 'lucide-svelte';

	import { Badge } from '$lib/components/ui/badge';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import {
		getAgeRangeLabels,
		getGenderLabels,
		getIncomeRangeLabels
	} from '$lib/components/brand/settings/audience/options';
	import type { ContentBriefCampaignGenerationJobResult } from '$lib/api/campaign-generation-jobs';
	import type { BrandAudience, ContentPillarParsed } from '$lib/api/brand-data/model/BrandData';

	type Props = {
		brief: ContentBriefCampaignGenerationJobResult | null;
		audiences: BrandAudience[];
		contentPillars: ContentPillarParsed[];
		isLoading: boolean;
		isJobActive: boolean;
	};

	let { brief, audiences, contentPillars, isLoading, isJobActive }: Props = $props();

	const matchedAudiences = $derived(
		brief ? audiences.filter((audience) => brief.targetAudienceIds.includes(audience.id)) : []
	);

	const matchedPillars = $derived(
		brief ? contentPillars.filter((pillar) => brief.contentPillarIds.includes(pillar.id)) : []
	);

	const durationDays = $derived.by(() => {
		if (!brief) return null;
		const start = new Date(brief.startDate);
		const end = new Date(brief.endDate);
		return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
	});

	const channelLabels: Record<string, string> = {
		instagram: 'Instagram',
		facebook: 'Facebook',
		tiktok: 'TikTok',
		linkedin: 'LinkedIn',
		youtube: 'YouTube',
		x: 'X',
		twitter: 'Twitter',
		pinterest: 'Pinterest',
		snapchat: 'Snapchat',
		reddit: 'Reddit',
		website: 'Website',
		blog: 'Blog',
		email: 'Email',
		newsletter: 'Newsletter'
	};

	const formatLabel = (value: string) =>
		value
			.replace(/[_-]+/g, ' ')
			.toLowerCase()
			.replace(/\b\w/g, (character) => character.toUpperCase());

	const toReadableChannelLabel = (channel: string) => {
		const normalized = channel.trim().toLowerCase();
		return channelLabels[normalized] ?? formatLabel(channel);
	};
</script>

{#if brief}
	<div class="w-full space-y-8">
		<div class="mb-6 text-center space-y-4" in:fade={{ duration: 400, delay: 100 }}>
			<div>
				<h2 class="text-3xl md:text-4xl font-bold">{brief.name}</h2>
				<div class="flex items-center justify-center gap-4 mt-3">
					{#if durationDays}
						<div class="flex items-center gap-2 text-sm text-muted-foreground">
							<Calendar class="w-4 h-4" />
							<span>{durationDays} days</span>
						</div>
					{/if}
					{#if brief.channels.length > 0}
						<div class="flex items-center gap-2">
							{#if brief.goal}
								<Badge variant="outline" class="text-xs rounded-full px-3 py-1">
									{formatLabel(brief.goal)}
								</Badge>
							{/if}
							{#each brief.channels as channel (channel)}
								<Badge variant="secondary" class="text-xs rounded-full px-3 py-1">
									{toReadableChannelLabel(channel)}
								</Badge>
							{/each}
						</div>
					{/if}
				</div>
			</div>
			{#if brief.description}
				<p class="text-base text-muted-foreground max-w-3xl mx-auto leading-relaxed">
					{brief.description}
				</p>
			{/if}
		</div>

		<div class="max-w-6xl mx-auto">
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
				{#if matchedAudiences.length > 0}
					<div class="space-y-4" in:fly={{ y: 30, duration: 600, delay: 300 }}>
						<div class="flex items-center gap-2">
							<Users class="w-4 h-4 text-muted-foreground" />
							<h3 class="font-semibold text-foreground">Target Audiences</h3>
						</div>
						<div class="flex flex-col gap-3">
							{#each matchedAudiences as audience (audience.id)}
								{@const genderLabel = getGenderLabels(audience.gender)}
								{@const ageLabel = getAgeRangeLabels(audience.ageRange)}
								{@const incomeLabel = getIncomeRangeLabels(audience.incomeRange)}
								<div
									class="flex flex-col gap-2 rounded-xl border bg-card/60 px-4 py-3"
								>
									<div class="flex flex-wrap gap-1.5 items-center">
										<Badge variant="default" class="text-xs rounded-full px-3 py-1">
											{audience.name}
										</Badge>
										<Badge variant="outline" class="text-xs rounded-full px-3 py-1 inline-flex items-center gap-1">
											<svelte:component this={genderLabel.icon} class="h-3 w-3 shrink-0" />
											{genderLabel.shortLabel}
										</Badge>
										<Badge variant="outline" class="text-xs rounded-full px-3 py-1 inline-flex items-center gap-1">
											<svelte:component this={ageLabel.icon} class="h-3 w-3 shrink-0" />
											{ageLabel.shortLabel}
										</Badge>
										<Badge variant="outline" class="text-xs rounded-full px-3 py-1 inline-flex items-center gap-1">
											<svelte:component this={incomeLabel.icon} class="h-3 w-3 shrink-0" />
											{incomeLabel.shortLabel}
										</Badge>
										{#each audience.channels as channel (channel)}
											<Badge variant="secondary" class="text-xs rounded-full px-3 py-1">
												{toReadableChannelLabel(channel)}
											</Badge>
										{/each}
									</div>
									{#if audience.painPoints.length > 0}
										<div class="flex flex-wrap gap-1.5 border-t border-border/60 pt-2">
											{#each audience.painPoints as painPoint (painPoint)}
												<span
													class="inline-flex max-w-full items-center rounded-full bg-muted px-2 py-0.5 text-[10px] leading-tight text-muted-foreground"
												>
													<span class="truncate">{painPoint}</span>
												</span>
											{/each}
										</div>
									{/if}
								</div>
							{/each}
						</div>
					</div>
				{/if}

				{#if matchedPillars.length > 0}
					<div class="space-y-4" in:fly={{ y: 30, duration: 600, delay: 400 }}>
						<div class="flex items-center gap-2">
							<Sparkles class="w-4 h-4 text-muted-foreground" />
							<h3 class="font-semibold text-foreground">Content Pillars</h3>
						</div>
						<div class="flex flex-col gap-3">
							{#each matchedPillars as pillar (pillar.id)}
								<div
									class="flex flex-col gap-2 rounded-xl border bg-card/60 px-4 py-3"
								>
									<p class="text-[11px] uppercase tracking-wide text-muted-foreground">
										Topic
									</p>
									<div class="flex flex-wrap gap-1.5 items-center">
										<Badge variant="default" class="text-xs rounded-full px-3 py-1">
											{pillar.name}
										</Badge>
										<Badge variant="outline" class="text-xs rounded-full px-3 py-1">
											{formatLabel(pillar.type)}
										</Badge>
										<Badge variant="outline" class="text-xs rounded-full px-3 py-1">
											{formatLabel(pillar.businessGoal)}
										</Badge>
										<Badge variant="outline" class="text-xs rounded-full px-3 py-1">
											{formatLabel(pillar.funnelStage)}
										</Badge>
									</div>
									{#if pillar.contentTypes.length > 0}
										<p class="text-[11px] uppercase tracking-wide text-muted-foreground pt-1 border-t border-border/60 mt-0.5">
											Content types
										</p>
										<div class="flex flex-wrap gap-1.5">
											{#each pillar.contentTypes as contentType (contentType)}
												<Badge variant="secondary" class="text-xs rounded-full px-3 py-1">
													{formatLabel(contentType)}
												</Badge>
											{/each}
										</div>
									{/if}
								</div>
							{/each}
						</div>
					</div>
				{/if}
			</div>
		</div>

		{#if isJobActive}
			<div class="max-w-6xl mx-auto" in:fly={{ y: 20, duration: 500, delay: 600 }}>
				<div
					class="flex items-center gap-3 rounded-lg border border-dashed px-5 py-4 text-muted-foreground"
				>
					<Loader2 class="w-4 h-4 animate-spin flex-shrink-0" />
					<span class="text-sm">Generating content plan…</span>
				</div>
			</div>
		{/if}
	</div>
{:else if isLoading}
	<div class="w-full">
		<div class="mb-6 text-center" in:fade={{ duration: 400 }}>
			<div class="h-10 bg-muted rounded animate-pulse w-2/3 mx-auto mb-2"></div>
			<div class="h-4 bg-muted rounded animate-pulse w-1/2 mx-auto"></div>
		</div>
		<div class="max-w-6xl mx-auto">
			<div in:fly={{ y: 30, duration: 600, delay: 200 }}>
				<Card>
					<CardHeader class="pb-4">
						<CardTitle class="flex items-center gap-2 text-base">
							<Loader2 class="w-4 h-4 animate-spin" />
							Generating Content Plan Brief
						</CardTitle>
					</CardHeader>
					<CardContent class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<div class="space-y-2">
							<div class="h-4 bg-muted rounded animate-pulse w-16"></div>
							<div class="h-5 bg-muted rounded animate-pulse"></div>
						</div>
						<div class="space-y-2">
							<div class="h-4 bg-muted rounded animate-pulse w-20"></div>
							<div class="h-5 bg-muted rounded animate-pulse w-24"></div>
						</div>
						<div class="space-y-2">
							<div class="h-4 bg-muted rounded animate-pulse w-20"></div>
							<div class="h-6 bg-muted rounded animate-pulse w-32"></div>
						</div>
					</CardContent>
				</Card>
			</div>
		</div>
	</div>
{/if}
