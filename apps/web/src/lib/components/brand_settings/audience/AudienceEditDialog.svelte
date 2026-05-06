<script lang="ts">
	import type { BrandAudience } from '$lib/api/brand-data/model/BrandData';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Plus, Trash2, X } from 'lucide-svelte';
	import type { SvelteComponent } from 'svelte';
	import {
		AGE_RANGE_OPTIONS,
		CHANNEL_OPTIONS,
		GENDER_OPTIONS,
		getAgeRangeLabels,
		getGenderLabels,
		getIncomeRangeLabels,
		INCOME_RANGE_OPTIONS
	} from './options';

	interface Props {
		audience: BrandAudience;
		open?: boolean;
		readonly?: boolean;
		onDelete?: () => void;
	}

	let {
		audience = $bindable(),
		open = $bindable(false),
		readonly = false,
		onDelete
	}: Props = $props();

	function updateAudience(patch: Partial<BrandAudience>) {
		if (readonly) return;
		audience = { ...audience, ...patch };
	}

	function updateArrayField(
		field: keyof Pick<BrandAudience, 'painPoints' | 'objections'>,
		index: number,
		value: string
	) {
		if (readonly) return;
		const next = [...audience[field]];
		next[index] = value;
		updateAudience({ [field]: next } as Partial<BrandAudience>);
	}

	function addArrayItem(field: keyof Pick<BrandAudience, 'painPoints' | 'objections'>) {
		if (readonly) return;
		const next = [...audience[field], ''];
		updateAudience({ [field]: next } as Partial<BrandAudience>);
	}

	function removeArrayItem(
		field: keyof Pick<BrandAudience, 'painPoints' | 'objections'>,
		index: number
	) {
		if (readonly) return;
		const next = audience[field].filter((_, i) => i !== index);
		updateAudience({ [field]: next } as Partial<BrandAudience>);
	}

	function toggleChannel(value: BrandAudience['channels'][number]) {
		if (readonly) return;
		const exists = audience.channels.includes(value);
		updateAudience({
			channels: exists
				? audience.channels.filter((c) => c !== value)
				: [...audience.channels, value]
		});
	}

	const ageLabel = $derived(getAgeRangeLabels(audience.ageRange));
	const genderLabel = $derived(getGenderLabels(audience.gender));
	const incomeLabel = $derived(getIncomeRangeLabels(audience.incomeRange));
</script>

<Dialog.Root bind:open>
	<Dialog.Content class="max-w-3xl max-h-[80vh] flex flex-col">
		<Dialog.Header>
			{#if readonly}
				<Dialog.Title>{audience.name || 'Untitled audience'}</Dialog.Title>
			{:else}
				<div class="flex flex-col gap-1">
					<Label class="text-xs text-muted-foreground">Audience name</Label>
					<Input
						value={audience.name}
						placeholder="e.g. Young professionals"
						oninput={(event) => updateAudience({ name: event.currentTarget.value })}
						class="h-9"
					/>
				</div>
			{/if}
		</Dialog.Header>

		<div class="flex-1 min-h-0 space-y-6 py-4 overflow-y-auto pr-2">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<div class="space-y-2">
					<Label>Age range</Label>
					{#if readonly}
						{@const AgeIcon = ageLabel.icon}
						<p class="flex items-center gap-2 text-sm text-muted-foreground py-2">
							<AgeIcon class="h-4 w-4" />
							<span>{ageLabel.fullLabel}</span>
						</p>
					{:else}
						<Select.Root
							type="single"
							value={audience.ageRange}
							onValueChange={(value) =>
								updateAudience({ ageRange: value as BrandAudience['ageRange'] })}
						>
							<Select.Trigger class="w-full">
								{@const AgeIcon = ageLabel.icon}
								<div class="flex items-center gap-2">
									<AgeIcon class="h-4 w-4" />
									<span>{ageLabel.shortLabel}</span>
								</div>
							</Select.Trigger>
							<Select.Content>
								{#each AGE_RANGE_OPTIONS as option (option.value)}
									{@const AgeIcon = option.icon}
									<Select.Item value={option.value} label={option.fullLabel}>
										<div class="flex items-center gap-2">
											<AgeIcon class="h-4 w-4" />
											<span>{option.fullLabel}</span>
										</div>
									</Select.Item>
								{/each}
							</Select.Content>
						</Select.Root>
					{/if}
				</div>

				<div class="space-y-2">
					<Label>Gender</Label>
					{#if readonly}
						{@const GenderIcon = genderLabel.icon}
						<p class="flex items-center gap-2 text-sm text-muted-foreground py-2">
							<GenderIcon class="h-4 w-4" />
							<span>{genderLabel.fullLabel}</span>
						</p>
					{:else}
						<Select.Root
							type="single"
							value={audience.gender}
							onValueChange={(value) =>
								updateAudience({ gender: value as BrandAudience['gender'] })}
						>
							<Select.Trigger class="w-full">
								{@const GenderIcon = genderLabel.icon}
								<div class="flex items-center gap-2">
									<GenderIcon class="h-4 w-4" />
									<span>{genderLabel.shortLabel}</span>
								</div>
							</Select.Trigger>
							<Select.Content>
								{#each GENDER_OPTIONS as option (option.value)}
									{@const GenderIcon = option.icon}
									<Select.Item value={option.value} label={option.fullLabel}>
										<div class="flex items-center gap-2">
											<GenderIcon class="h-4 w-4" />
											<span>{option.fullLabel}</span>
										</div>
									</Select.Item>
								{/each}
							</Select.Content>
						</Select.Root>
					{/if}
				</div>

				<div class="space-y-2">
					<Label>Income range</Label>
					{#if readonly}
						{@const IncomeIcon = incomeLabel.icon}
						<p class="flex items-center gap-2 text-sm text-muted-foreground py-2">
							<IncomeIcon class="h-4 w-4" />
							<span>{incomeLabel.fullLabel}</span>
						</p>
					{:else}
						<Select.Root
							type="single"
							value={audience.incomeRange}
							onValueChange={(value) =>
								updateAudience({ incomeRange: value as BrandAudience['incomeRange'] })}
						>
							<Select.Trigger class="w-full">
								{@const IncomeIcon = incomeLabel.icon}
								<div class="flex items-center gap-2">
									<IncomeIcon class="h-4 w-4" />
									<span>{incomeLabel.shortLabel}</span>
								</div>
							</Select.Trigger>
							<Select.Content>
								{#each INCOME_RANGE_OPTIONS as option (option.value)}
									{@const IncomeIcon = option.icon}
									<Select.Item value={option.value} label={option.fullLabel}>
										<div class="flex items-center gap-2">
											<IncomeIcon class="h-4 w-4" />
											<span>{option.fullLabel}</span>
										</div>
									</Select.Item>
								{/each}
							</Select.Content>
						</Select.Root>
					{/if}
				</div>
			</div>

			<div class="space-y-4">
				<div class="space-y-4">
					<div class="space-y-2">
						<Label>Pain points</Label>
						<div class="space-y-1">
							<p class="text-xs text-muted-foreground">
								The biggest frustration you are addressing.
							</p>
							{#each audience.painPoints as item, index (index)}
								<div class="flex items-start gap-2">
									<Textarea
										class="w-full  rounded-xl"
										value={item}
										placeholder="Describe a pain point"
										oninput={(event) =>
											updateArrayField('painPoints', index, event.currentTarget.value)}
									/>
									{#if !readonly}
										<Button
											type="button"
											size="icon"
											variant="ghost"
											class="shrink-0 btn-rounded-full"
											onclick={() => removeArrayItem('painPoints', index)}
										>
											<X class="h-4 w-4" />
										</Button>
									{/if}
								</div>
							{/each}
							{#if !readonly}
								<Button
									type="button"
									variant="outline"
									size="sm"
									class="mt-1 btn-rounded-full"
									onclick={() => addArrayItem('painPoints')}
								>
									<Plus class="h-3 w-3 mr-1" />
									Add pain point
								</Button>
							{/if}
						</div>
					</div>

					<div class="space-y-2">
						<Label>Objections</Label>
						<div class="space-y-1">
							<p class="text-xs text-muted-foreground">
								What stops them from interacting with you.
							</p>
							{#each audience.objections as item, index (index)}
								<div class="flex items-start gap-2">
									<Textarea
										class="w-full rounded-xl"
										value={item}
										placeholder="Describe an objection"
										oninput={(event) =>
											updateArrayField('objections', index, event.currentTarget.value)}
									/>
									{#if !readonly}
										<Button
											type="button"
											size="icon"
											variant="ghost"
											class="shrink-0 btn-rounded-full"
											onclick={() => removeArrayItem('objections', index)}
										>
											<X class="h-4 w-4" />
										</Button>
									{/if}
								</div>
							{/each}
							{#if !readonly}
								<Button
									type="button"
									variant="outline"
									size="sm"
									class="mt-1 btn-rounded-full"
									onclick={() => addArrayItem('objections')}
								>
									<Plus class="h-3 w-3 mr-1" />
									Add objection
								</Button>
							{/if}
						</div>
					</div>
				</div>
			</div>

			<div class="space-y-2">
				<Label>Channels</Label>
				<div class="flex flex-wrap gap-2">
					{#each CHANNEL_OPTIONS as option (option.value)}
						{@const isSelected = audience.channels.includes(option.value)}
						{@const Icon = option.icon as typeof SvelteComponent}
						<button
							type="button"
							class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs transition-colors
								{isSelected
								? 'bg-primary text-primary-foreground border-primary'
								: 'bg-background text-muted-foreground hover:bg-muted'}"
							onclick={() => toggleChannel(option.value)}
							disabled={readonly}
						>
							<Icon class="h-3 w-3" />
							<span>{option.fullLabel}</span>
						</button>
					{/each}
				</div>
			</div>
		</div>

		<Dialog.Footer class="flex justify-between">
			<div class="flex w-full items-center justify-between">
				{#if !readonly && onDelete}
					<Button
						type="button"
						variant="ghost"
						class="text-destructive hover:bg-destructive/5 cursor-pointer rounded-full"
						onclick={() => {
							onDelete();
							open = false;
						}}
					>
						<Trash2 class="mr-2 h-4 w-4" />
						Delete
					</Button>
				{/if}
				<Button type="button" variant="outline" class="ml-auto" onclick={() => (open = false)}>
					Done
				</Button>
			</div>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
