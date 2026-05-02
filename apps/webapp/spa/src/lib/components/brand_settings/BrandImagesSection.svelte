<script lang="ts">
	import type { BrandSettingsFormData } from './form-data';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Image as ImageIcon } from 'lucide-svelte';

	interface Props {
		data: BrandSettingsFormData;
		readonly?: boolean;
	}

	let { data = $bindable(), readonly = false }: Props = $props();

	const mediaUrls = $derived(data.mediaUrls ?? []);
	const hasImages = $derived(mediaUrls.length > 0);
</script>

{#if hasImages}
	<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80">
		<CardHeader>
			<CardTitle class="flex items-center gap-2">
				<ImageIcon class="h-5 w-5 text-purple-600" />
				Brand Images
			</CardTitle>
		</CardHeader>
		<CardContent>
			<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
				{#each mediaUrls.slice(0, 12) as imageUrl (imageUrl)}
					<div class="group relative aspect-square overflow-hidden rounded-lg shadow-md">
						<img
							src={imageUrl}
							alt="Brand"
							class="h-full w-full object-cover transition-transform group-hover:scale-110"
						/>
					</div>
				{/each}
			</div>
		</CardContent>
	</Card>
{/if}
