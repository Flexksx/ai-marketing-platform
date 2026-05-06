<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Image as ImageIcon, X } from 'lucide-svelte';

	type Props = {
		mediaUrls: string[];
	};

	let { mediaUrls }: Props = $props();

	let showGallery = $state(false);
</script>

<Card
	class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80 cursor-pointer transition-shadow hover:shadow-2xl"
	role="button"
	tabindex={0}
	onclick={() => mediaUrls.length > 0 && (showGallery = true)}
	onkeydown={(e) => e.key === 'Enter' && mediaUrls.length > 0 && (showGallery = true)}
	aria-label="View brand images"
>
	<CardHeader>
		<CardTitle class="flex items-center gap-2">
			<ImageIcon class="h-5 w-5 text-purple-600" /> Brand Images
		</CardTitle>
	</CardHeader>
	<CardContent>
		{#if mediaUrls.length > 0}
			<div class="flex flex-nowrap gap-3 overflow-x-auto pb-1">
				{#each mediaUrls as img, i (img + '_' + i)}
					<div
						class="h-20 w-20 shrink-0 overflow-hidden rounded-lg shadow-md ring-1 ring-black/5"
					>
						<img src={img} alt="Brand image {i + 1}" class="h-full w-full object-cover" />
					</div>
				{/each}
			</div>
			<p class="mt-2 text-sm text-muted-foreground">
				{mediaUrls.length} image{mediaUrls.length === 1 ? '' : 's'} — click to view all
			</p>
		{:else}
			<div class="flex items-center gap-2 py-4 text-muted-foreground">
				<ImageIcon class="h-8 w-8 shrink-0 opacity-50" />
				<span>No images uploaded yet.</span>
			</div>
		{/if}
	</CardContent>
</Card>

{#if mediaUrls.length > 0}
	<Dialog.Root bind:open={showGallery}>
		<Dialog.Content class="max-w-4xl max-h-[90vh] flex flex-col">
			<Dialog.Header>
				<Dialog.Title>Brand Images</Dialog.Title>
				<Dialog.Description
					>All {mediaUrls.length} image{mediaUrls.length === 1 ? '' : 's'}</Dialog.Description
				>
			</Dialog.Header>
			<div class="flex-1 overflow-y-auto py-4">
				<div class="grid grid-cols-2 gap-4 sm:grid-cols-3">
					{#each mediaUrls as img, i (img + '_' + i)}
						<button
							type="button"
							class="group relative aspect-square overflow-hidden rounded-lg bg-muted shadow-md ring-1 ring-black/5 focus:outline-none focus:ring-2 focus:ring-primary text-left"
							onclick={() => window.open(img, '_blank', 'noopener,noreferrer')}
						>
							<img
								src={img}
								alt="Brand image {i + 1}"
								class="h-full w-full object-cover transition-transform group-hover:scale-105"
							/>
						</button>
					{/each}
				</div>
			</div>
			<Dialog.Footer>
				<Button variant="outline" onclick={() => (showGallery = false)}>
					<X class="h-4 w-4 mr-2" /> Close
				</Button>
			</Dialog.Footer>
		</Dialog.Content>
	</Dialog.Root>
{/if}
