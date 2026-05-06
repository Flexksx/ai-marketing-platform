<script lang="ts">
	import FloatingImage from '$lib/components/brand/floating-image.svelte';
	import { Loader2, Sparkles } from 'lucide-svelte';
	import { fade } from 'svelte/transition';

	type Props = {
		mode?: 'extracting' | 'analyzing';
		scraperResult?: {
			screenshot?: string | null;
			logo?: string | null;
			image_urls?: string[];
		} | null;
	};

	let { mode = 'extracting', scraperResult = null }: Props = $props();

	let currentMessageIndex = $state(0);

	const extractionMessages = [
		'We are extracting your brand identity...',
		'Analyzing your website content...',
		'Discovering your brand colors...',
		'Identifying your brand voice...',
		'Understanding your audience...',
		'Building your brand profile...'
	];

	$effect(() => {
		if (mode === 'extracting') {
			const interval = setInterval(() => {
				currentMessageIndex = (currentMessageIndex + 1) % extractionMessages.length;
			}, 2000);
			return () => clearInterval(interval);
		}
	});
</script>

{#if mode === 'extracting'}
	<div class="flex flex-col items-center justify-center min-h-screen px-4">
		<div class="relative w-full max-w-2xl">
			<div class="absolute inset-0 pointer-events-none">
				<Sparkles
					class="absolute top-1/4 left-1/3 w-6 h-6 text-primary/40 animate-pulse"
					style="animation-delay: 0.5s;"
				/>
				<Sparkles
					class="absolute top-1/3 right-1/4 w-5 h-5 text-blue-400/40 animate-pulse"
					style="animation-delay: 1.2s;"
				/>
				<Sparkles
					class="absolute bottom-1/3 left-1/4 w-7 h-7 text-purple-400/40 animate-pulse"
					style="animation-delay: 0.8s;"
				/>
				<Sparkles
					class="absolute top-2/3 right-1/3 w-4 h-4 text-green-400/40 animate-pulse"
					style="animation-delay: 1.8s;"
				/>
			</div>

			<div
				class="relative z-10 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-12 border border-border/50 shadow-xl"
			>
				<div class="text-center space-y-8">
					<div class="relative inline-block">
						<div class="absolute inset-0 animate-ping">
							<Sparkles class="w-16 h-16 text-primary/30" />
						</div>
						<Sparkles class="w-16 h-16 text-primary animate-pulse relative z-10" />
					</div>

					<div class="relative h-[4rem] flex items-center justify-center">
						{#key currentMessageIndex}
							<p
								class="text-xl font-medium text-foreground absolute"
								in:fade={{ duration: 400 }}
								out:fade={{ duration: 200 }}
							>
								{extractionMessages[currentMessageIndex]}
							</p>
						{/key}
					</div>

					<div class="flex justify-center">
						<Loader2 class="w-8 h-8 text-primary animate-spin" />
					</div>
				</div>
			</div>
		</div>
	</div>
{:else if mode === 'analyzing'}
	<div class="relative min-h-screen w-full overflow-hidden">
		{#if scraperResult?.image_urls}
			{#each scraperResult.image_urls.slice(0, 12) as imageUrl, index (imageUrl)}
				<FloatingImage {imageUrl} {index} />
			{/each}
		{/if}

		<div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
			<div class="max-w-4xl w-full space-y-8">
				{#if scraperResult?.screenshot}
					<div class="flex justify-center">
						<div class="relative">
							<img
								src={scraperResult.screenshot}
								alt="Website screenshot"
								class="relative rounded-2xl shadow-2xl border-4 border-white/50 max-w-full h-auto"
								style="max-height: 60vh;"
							/>
						</div>
					</div>
				{/if}

				<div class="text-center space-y-4">
					{#if scraperResult?.logo}
						<div class="flex justify-center mb-4">
							<div
								class="h-24 w-24 rounded-full overflow-hidden shadow-xl border-4 border-white/50 bg-white p-2"
							>
								<img
									src={scraperResult.logo}
									alt="Brand logo"
									class="h-full w-full object-contain"
								/>
							</div>
						</div>
					{/if}

					<h2 class="text-4xl md:text-5xl font-bold text-foreground">
						{scraperResult?.logo ? 'Analyzing Your Brand...' : 'Analyzing Your Website...'}
					</h2>

					<p class="text-lg text-muted-foreground" style="font-family: var(--font-body);">
						We're processing your brand identity with AI
					</p>

					<div class="flex justify-center pt-4">
						<Loader2 class="w-8 h-8 text-primary animate-spin" />
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
