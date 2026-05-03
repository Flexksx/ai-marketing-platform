<script lang="ts">
	import { useBrandEditorStore } from './BrandEditorStore.svelte';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Image as ImageIcon } from 'lucide-svelte';

	interface Props {
		readonly?: boolean;
	}

	let { readonly = false }: Props = $props();

	const store = useBrandEditorStore();
</script>

{#if store.mediaUrls.length > 0}
	<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80">
		<CardHeader>
			<CardTitle class="flex items-center gap-2">
				<ImageIcon class="h-5 w-5 text-purple-600" />
				Brand Images
			</CardTitle>
		</CardHeader>
		<CardContent>
			<div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
				{#each store.mediaUrls.slice(0, 12) as imageUrl (imageUrl)}
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
