<script lang="ts">
	import { defaultToneOfVoice, type BrandSettingsFormData } from '$lib/api/brands/model/BrandData';
	import JargonSlider from '$lib/components/brand_settings/JargonSlider.svelte';
	import SentenceLengthSelect from '$lib/components/brand_settings/SentenceLengthSelect.svelte';
	import ToneDimensionSlider from '$lib/components/brand_settings/ToneDimensionSlider.svelte';
	import ToneWordList from '$lib/components/brand_settings/ToneWordList.svelte';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Package } from 'lucide-svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
	}

	let { data = $bindable(), readonly = false }: Props = $props();

	function ensureToneOfVoice() {
		if (!data.toneOfVoice) {
			data.toneOfVoice = { ...defaultToneOfVoice };
		}
	}

	$effect(() => {
		if (!readonly) ensureToneOfVoice();
	});
</script>

<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80 h-full">
	<CardContent class="p-6">
		<div class="mb-4 flex items-center justify-between">
			<h3 class="text-lg font-semibold flex items-center gap-2">
				<Package class="h-5 w-5 text-green-600" />
				Tone of Voice
			</h3>
		</div>
		<div>
			{#if data.toneOfVoice}
				<div class="space-y-4">
					<div class="space-y-4">
						<ToneDimensionSlider
							dimensionKey="formality"
							bind:value={data.toneOfVoice.formality_level}
							{readonly}
						/>
						<ToneDimensionSlider
							dimensionKey="humour"
							bind:value={data.toneOfVoice.humour_level}
							{readonly}
						/>
						<ToneDimensionSlider
							dimensionKey="irreverence"
							bind:value={data.toneOfVoice.irreverence_level}
							{readonly}
						/>
						<ToneDimensionSlider
							dimensionKey="enthusiasm"
							bind:value={data.toneOfVoice.enthusiasm_level}
							{readonly}
						/>
						<JargonSlider
							bind:value={data.toneOfVoice.industry_jargon_usage_level}
							{readonly}
						/>
						<SentenceLengthSelect
							bind:value={data.toneOfVoice.sentence_length_preference}
							{readonly}
						/>
					</div>
					<ToneWordList
						title="Sensory Keywords"
						bind:words={data.toneOfVoice.sensory_keywords}
						variant="sensory"
						{readonly}
					/>
					<ToneWordList
						title="Excluded Words"
						bind:words={data.toneOfVoice.excluded_words}
						variant="excluded"
						{readonly}
					/>
					<ToneWordList
						title="Signature Words"
						bind:words={data.toneOfVoice.signature_words}
						variant="signature"
						{readonly}
					/>
				</div>
			{:else}
				<p class="text-muted-foreground italic">No tone of voice data yet...</p>
			{/if}
		</div>
	</CardContent>
</Card>
