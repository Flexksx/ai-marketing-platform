<script lang="ts">
	import type { BrandSettingsFormData } from './form-data';
	import { getLanguageName, ISO_639_1_LANGUAGE_CODES } from '$lib/utils/language';
	import MarkdownRenderer from '$lib/components/markdown/MarkdownRenderer.svelte';
	import BrandColorsSection from './BrandColorsSection.svelte';
	import BrandLogoUpload from './BrandLogoUpload.svelte';
	import PositioningSection from './PositioningSection.svelte';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import * as Select from '$lib/components/ui/select';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Building2, Languages } from 'lucide-svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
	}

	const NONE_VALUE = '';

	let { data = $bindable(), readonly = false }: Props = $props();

	let isEditingName = $state(false);
	let editName = $state('');

	let isEditingMission = $state(false);
	let editMission = $state('');

	let isEditingDescription = $state(false);
	let editDescription = $state('');

	let selectedLocaleCode = $state('');

	$effect(() => {
		selectedLocaleCode = data.locale ?? NONE_VALUE;
	});
	$effect(() => {
		data.locale = selectedLocaleCode === NONE_VALUE ? null : selectedLocaleCode;
	});

	const localeLabel = $derived(
		data.locale ? getLanguageName(data.locale) ?? data.locale : null
	);

	const languageOptionsSorted = $derived(
		[...ISO_639_1_LANGUAGE_CODES]
			.map((code) => ({ code, label: getLanguageName(code) ?? code }))
			.sort((a, b) => a.label.localeCompare(b.label))
	);

	const selectTriggerLabel = $derived(
		selectedLocaleCode === NONE_VALUE ? 'Select language' : (localeLabel ?? selectedLocaleCode)
	);

	function startEditName() {
		editName = data.name;
		isEditingName = true;
	}

	function commitName() {
		data.name = editName.trim();
		isEditingName = false;
	}

	function cancelName() {
		isEditingName = false;
	}

	function startEditMission() {
		editMission = data.brandMission;
		isEditingMission = true;
	}

	function commitMission() {
		data.brandMission = editMission.trim();
		isEditingMission = false;
	}

	function cancelMission() {
		isEditingMission = false;
	}

	function startEditDescription() {
		editDescription = data.description;
		isEditingDescription = true;
	}

	function commitDescription() {
		data.description = editDescription.trim();
		isEditingDescription = false;
	}

	function cancelDescription() {
		isEditingDescription = false;
	}
</script>

<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80 h-full">
	<CardContent class="p-6 h-full flex flex-col">
		<div class="flex items-start gap-4 mb-4">
			<BrandLogoUpload
				logoUrl={data.logoUrl}
				brandName={data.name}
				pendingFile={data.pendingLogoFile}
				onFileSelected={(file) => (data.pendingLogoFile = file)}
				{readonly}
			/>
			<div class="flex-1 min-w-0">
				<div class="flex flex-wrap items-center justify-between gap-4">
					{#if !readonly && isEditingName}
						<Input
							bind:value={editName}
							class="text-xl font-bold h-auto py-0.5 px-1"
							autofocus
							onblur={commitName}
							onkeydown={(e: KeyboardEvent) => {
								if (e.key === 'Escape') cancelName();
								if (e.key === 'Enter') { e.preventDefault(); commitName(); }
							}}
						/>
					{:else if readonly}
						<h3 class="text-xl font-bold">{data.name || 'Brand Name'}</h3>
					{:else}
						<button
							type="button"
							class="text-xl font-bold cursor-pointer hover:text-muted-foreground transition-colors text-left bg-transparent border-0 p-0"
							onclick={startEditName}
						>
							{data.name || 'Brand Name'}
						</button>
					{/if}
					<div class="flex items-center gap-3">
						<BrandColorsSection bind:data={data} readonly={readonly} variant="inline" />
					</div>
				</div>
			</div>
		</div>

		<div class="flex-1 space-y-4">
			<div>
				<div class="mb-2 flex items-center justify-between">
					<p class="text-muted-foreground text-sm flex items-center gap-2">
						<Building2 class="h-4 w-4" />
						Brand Mission
					</p>
				</div>
				{#if !readonly && isEditingMission}
					<Textarea
						bind:value={editMission}
						class="min-h-[100px] resize-y text-sm"
						autofocus
						onblur={commitMission}
						onkeydown={(e: KeyboardEvent) => {
							if (e.key === 'Escape') cancelMission();
							if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { e.preventDefault(); commitMission(); }
						}}
					/>
				{:else if readonly}
					<div>
						{#if data.brandMission}
							<MarkdownRenderer content={data.brandMission} />
						{:else}
							<p class="text-muted-foreground italic text-sm">No mission statement yet...</p>
						{/if}
					</div>
				{:else}
					<div
						class="cursor-pointer hover:bg-muted/50 rounded-md p-1 -m-1 transition-colors"
						onclick={startEditMission}
						onkeydown={(e: KeyboardEvent) => {
							if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); startEditMission(); }
						}}
						role="button"
						tabindex={0}
					>
						{#if data.brandMission}
							<MarkdownRenderer content={data.brandMission} />
						{:else}
							<p class="text-muted-foreground italic text-sm">No mission statement yet...</p>
						{/if}
					</div>
				{/if}
			</div>
			<div>
				<div class="mb-2 flex items-center justify-between">
					<p class="text-muted-foreground text-sm flex items-center gap-2">
						Description
					</p>
				</div>
				{#if !readonly && isEditingDescription}
					<Textarea
						bind:value={editDescription}
						class="min-h-[100px] resize-y text-sm"
						autofocus
						onblur={commitDescription}
						onkeydown={(e: KeyboardEvent) => {
							if (e.key === 'Escape') cancelDescription();
							if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { e.preventDefault(); commitDescription(); }
						}}
					/>
				{:else if readonly}
					<div>
						{#if data.description}
							<p class="text-sm">{data.description}</p>
						{:else}
							<p class="text-muted-foreground italic text-sm">No description yet...</p>
						{/if}
					</div>
				{:else}
					<div
						class="cursor-pointer hover:bg-muted/50 rounded-md p-1 -m-1 transition-colors"
						onclick={startEditDescription}
						onkeydown={(e: KeyboardEvent) => {
							if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); startEditDescription(); }
						}}
						role="button"
						tabindex={0}
					>
						{#if data.description}
							<p class="text-sm">{data.description}</p>
						{:else}
							<p class="text-muted-foreground italic text-sm">No description yet...</p>
						{/if}
					</div>
				{/if}
			</div>
			<div>
				<div class="mb-2 flex items-center justify-between">
					<p class="text-muted-foreground text-sm flex items-center gap-2">
						<Languages class="h-4 w-4" />
						Language
					</p>
				</div>
				{#if readonly}
					<p class="text-sm">{localeLabel ?? '—'}</p>
				{:else}
					<Select.Root type="single" bind:value={selectedLocaleCode}>
						<Select.Trigger class="w-full h-10">
							{selectTriggerLabel}
						</Select.Trigger>
						<Select.Content class="max-h-[300px]">
							<Select.Item value={NONE_VALUE} label="None">
								None
							</Select.Item>
							{#each languageOptionsSorted as option (option.code)}
								<Select.Item value={option.code} label={option.label}>
									{option.label}
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
				{/if}
			</div>

			<PositioningSection bind:data={data} {readonly} />
		</div>
	</CardContent>
</Card>

