<script lang="ts">
	import MarkdownRenderer from '$lib/components/markdown/MarkdownRenderer.svelte';
	import type { BrandSettingsFormData } from '$lib/components/brand_settings/form-data';
	import type { BrandArchetypeName } from '$lib/api/generated/models/BrandArchetypeName';
	import { getArchetypeDescription, getArchetypeLabel } from '$lib/utils/brandArchetype';
	import { BrandColorsSection, BrandLogoUpload } from '$lib/components/brand_settings';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Edit3, Sparkles } from 'lucide-svelte';

	type Props = {
		data: BrandSettingsFormData;
		onEditClick: () => void;
		onFileSelected?: (file: File) => void;
		readonly?: boolean;
	};

	let { data, onEditClick, onFileSelected, readonly = false }: Props = $props();

	const archetype = $derived(data.toneOfVoice?.archetype ?? null);
</script>

<Card
	class="group cursor-pointer border-0 bg-white/80 shadow-xl backdrop-blur-sm transition-all hover:-translate-y-1 hover:shadow-2xl dark:bg-slate-800/80"
	onclick={onEditClick}
	role="button"
	tabindex={0}
	onkeydown={(e) => e.key === 'Enter' && onEditClick()}
>
	<CardContent class="p-8 space-y-6">
		<div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
			<div class="flex items-start gap-4">
				<BrandLogoUpload
					logoUrl={data.logoUrl}
					brandName={data.name}
					pendingFile={data.pendingLogoFile}
					onFileSelected={(file) => onFileSelected?.(file)}
					{readonly}
				/>
				<div class="flex-1 min-w-0">
					<h3 class="text-xl font-bold mb-1">{data.name || 'Brand Name'}</h3>
					<p class="text-sm text-muted-foreground">Brand identity overview</p>
				</div>
			</div>

			<div class="flex flex-wrap items-center justify-start gap-3 md:justify-end">
				<BrandColorsSection bind:data={data} readonly={readonly} variant="inline" />
			</div>
		</div>

		<div class="max-w-5xl text-left">
			<MarkdownRenderer content={data.description || 'No description yet...'} />
		</div>

		{#if archetype}
			<div class="flex flex-col gap-1">
				<div class="flex items-center gap-2">
					<Sparkles class="h-4 w-4 text-muted-foreground" />
					<span class="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
						{getArchetypeLabel(archetype as BrandArchetypeName)}
					</span>
				</div>
				<p class="text-sm text-muted-foreground italic pl-6">
					{getArchetypeDescription(archetype as BrandArchetypeName)}
				</p>
			</div>
		{/if}

		{#if !readonly}
			<div class="mt-2 flex justify-end">
				<Edit3 class="h-5 w-5 text-slate-400" />
			</div>
		{/if}
	</CardContent>
</Card>
