<script lang="ts">
	import type { BrandAudience } from '$lib/api/generated/models/BrandAudience';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import * as Select from '$lib/components/ui/select';
	import { Pencil } from 'lucide-svelte';
	import type { SvelteComponent } from 'svelte';
	import AudienceCardListItem from './AudienceCardListItem.svelte';
	import {
		AGE_RANGE_OPTIONS,
		GENDER_OPTIONS,
		INCOME_RANGE_OPTIONS,
		getAgeRangeLabels,
		getChannelOption,
		getGenderLabels,
		getIncomeRangeLabels
	} from './options';

	interface Props {
		audience: BrandAudience;
		readonly?: boolean;
		onEditRequested?: () => void;
	}

	let { audience = $bindable(), readonly = false, onEditRequested }: Props = $props();

	function updateAudience(patch: Partial<BrandAudience>) {
		if (readonly) return;
		audience = { ...audience, ...patch };
	}

	const ageLabel = $derived(getAgeRangeLabels(audience.ageRange ?? 'ANY'));
	const genderLabel = $derived(getGenderLabels(audience.gender ?? 'ANY'));
	const incomeLabel = $derived(getIncomeRangeLabels(audience.incomeRange ?? 'ANY'));

	const channelBadges = $derived((audience.channels ?? []).map((item) => getChannelOption(item)));
</script>

<Card
	class="border bg-card/60 backdrop-blur-sm hover:bg-card transition-colors cursor-pointer rounded-3xl"
	onclick={() => {
		if (readonly || !onEditRequested) return;
		onEditRequested();
	}}
>
	<CardHeader class="flex flex-row items-start justify-between gap-4">
		<div class="flex flex-col gap-1">
			<CardTitle class="text-sm font-semibold">
				<span class="break-words">{audience.name || 'Untitled audience'}</span>
			</CardTitle>

			{#if channelBadges.length > 0}
				<div class="flex flex-wrap gap-1.5">
					{#each channelBadges as channel (channel.value)}
						{@const Icon = channel.icon as typeof SvelteComponent}
						<span
							class="inline-flex items-center justify-center rounded-full bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground"
						>
							<Icon class="h-3 w-3" />
						</span>
					{/each}
				</div>
			{/if}
		</div>
		{#if !readonly && onEditRequested}
			<Button
				type="button"
				size="icon"
				variant="ghost"
				class="h-7 w-7 shrink-0"
				onclick={(event) => {
					event.stopPropagation();
					onEditRequested();
				}}
			>
				<Pencil class="h-3 w-3" />
			</Button>
		{/if}
	</CardHeader>
	<CardContent class="space-y-3 pt-0">
		<div class="grid grid-cols-3 gap-3 text-xs">
			<div class="space-y-1">
				<p class="text-[11px] uppercase tracking-wide text-muted-foreground">Age</p>
				{#if readonly}
					{@const AgeIcon = ageLabel.icon}
					<p class="flex items-center gap-1">
						<AgeIcon class="h-3 w-3" />
						<span>{ageLabel.shortLabel}</span>
					</p>
				{:else}
					<Select.Root
						type="single"
						value={audience.ageRange}
						onValueChange={(value) =>
							updateAudience({ ageRange: value as BrandAudience['ageRange'] })}
					>
						<Select.Trigger class="h-8 text-xs">
							{@const AgeIcon = ageLabel.icon}
							<div class="flex items-center gap-1">
								<AgeIcon class="h-3 w-3" />
								<span>{ageLabel.shortLabel}</span>
							</div>
						</Select.Trigger>
						<Select.Content>
							{#each AGE_RANGE_OPTIONS as option (option.value)}
								{@const AgeIcon = option.icon}
								<Select.Item value={option.value} label={option.fullLabel}>
									<div class="flex items-center gap-1">
										<AgeIcon class="h-3 w-3" />
										<span>{option.shortLabel}</span>
									</div>
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
				{/if}
			</div>

			<div class="space-y-1">
				<p class="text-[11px] uppercase tracking-wide text-muted-foreground">Gender</p>
				{#if readonly}
					{@const GenderIcon = genderLabel.icon}
					<p class="flex items-center gap-1">
						<GenderIcon class="h-3 w-3" />
						<span>{genderLabel.shortLabel}</span>
					</p>
				{:else}
					<Select.Root
						type="single"
						value={audience.gender}
						onValueChange={(value) => updateAudience({ gender: value as BrandAudience['gender'] })}
					>
						<Select.Trigger class="h-8 text-xs">
							{@const GenderIcon = genderLabel.icon}
							<div class="flex items-center gap-1">
								<GenderIcon class="h-3 w-3" />
								<span>{genderLabel.shortLabel}</span>
							</div>
						</Select.Trigger>
						<Select.Content>
							{#each GENDER_OPTIONS as option (option.value)}
								{@const GenderIcon = option.icon}
								<Select.Item value={option.value} label={option.fullLabel}>
									<div class="flex items-center gap-1">
										<GenderIcon class="h-3 w-3" />
										<span>{option.shortLabel}</span>
									</div>
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
				{/if}
			</div>

			<div class="space-y-1">
				<p class="text-[11px] uppercase tracking-wide text-muted-foreground">Income</p>
				{#if readonly}
					{@const IncomeIcon = incomeLabel.icon}
					<p class="flex items-center gap-1">
						<IncomeIcon class="h-3 w-3" />
						<span>{incomeLabel.shortLabel}</span>
					</p>
				{:else}
					<Select.Root
						type="single"
						value={audience.incomeRange}
						onValueChange={(value) =>
							updateAudience({ incomeRange: value as BrandAudience['incomeRange'] })}
					>
						<Select.Trigger class="h-8 text-xs">
							{@const IncomeIcon = incomeLabel.icon}
							<div class="flex items-center gap-1">
								<IncomeIcon class="h-3 w-3" />
								<span>{incomeLabel.shortLabel}</span>
							</div>
						</Select.Trigger>
						<Select.Content>
							{#each INCOME_RANGE_OPTIONS as option (option.value)}
								{@const IncomeIcon = option.icon}
								<Select.Item value={option.value} label={option.fullLabel}>
									<div class="flex items-center gap-1">
										<IncomeIcon class="h-3 w-3" />
										<span>{option.shortLabel}</span>
									</div>
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
				{/if}
			</div>
		</div>

		<div class="space-y-2">
			{#if (audience.painPoints ?? []).length > 0}
				<div class="space-y-1">
					<p class="text-[11px] uppercase tracking-wide text-muted-foreground">Pain points</p>
					<div class="flex flex-wrap gap-1.5">
						{#each (audience.painPoints ?? []) as painPoint, index (index)}
							<AudienceCardListItem text={painPoint} />
						{/each}
					</div>
				</div>
			{/if}

			{#if (audience.objections ?? []).length > 0}
				<div class="space-y-1">
					<p class="text-[11px] uppercase tracking-wide text-muted-foreground">Objections</p>
					<div class="flex flex-wrap gap-1.5">
						{#each (audience.objections ?? []) as objection, index (index)}
							<AudienceCardListItem text={objection} />
						{/each}
					</div>
				</div>
			{/if}
		</div>
	</CardContent>
</Card>
