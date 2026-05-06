<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { fade } from 'svelte/transition';
	import NotFoundPage from '$lib/components/error/not-found-page.svelte';
	import type { ErrorPageData } from '$app/types';

	let { data }: { data: ErrorPageData } = $props();

	const status = data.status || 500;
	const isDevelopment = import.meta.env.DEV;

	// Sparkle system
	type Sparkle = {
		id: number;
		x: number;
		delay: number;
		duration: number;
		size: number;
		opacity: number;
		drift: number;
	};

	const sparkles = $state<Sparkle[]>([]);
	const sparkleCount = 50;

	// Initialize sparkles
	$effect(() => {
		const newSparkles: Sparkle[] = [];
		for (let i = 0; i < sparkleCount; i++) {
			newSparkles.push({
				id: i,
				x: Math.random() * 100,
				delay: Math.random() * 8,
				duration: 10 + Math.random() * 10,
				size: 6 + Math.random() * 12,
				opacity: 0.6 + Math.random() * 0.4,
				drift: (Math.random() - 0.5) * 2 // -1 to 1 for horizontal drift
			});
		}
		sparkles.length = 0;
		sparkles.push(...newSparkles);
	});
</script>

{#if status === 404}
	<NotFoundPage />
{:else}
	<div class="error-page-container">
		<!-- Wavy gradient background -->
		<div class="gradient-background"></div>

		<!-- Sparkles -->
		<div class="sparkles-container">
			{#each sparkles as sparkle (sparkle.id)}
				<div
					class="sparkle"
					style="left: {sparkle.x}%; animation-delay: {sparkle.delay}s; animation-duration: {sparkle.duration}s; width: {sparkle.size}px; height: {sparkle.size}px; opacity: {sparkle.opacity}; --drift: {sparkle.drift};"
				></div>
			{/each}
		</div>

		<!-- Content -->
		<div class="flex min-h-screen items-center justify-center px-4 relative z-10">
			<div class="w-full max-w-md text-center">
				<div class="mb-8" transition:fade={{ duration: 600, delay: 300 }}>
					<h1
						class="mb-6 text-5xl font-bold bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-shimmer dark:from-blue-400 dark:via-purple-400 dark:to-pink-400"
					>
						Hey, we're having some troubles on our end
					</h1>
					<p
						class="mb-4 text-xl text-foreground/90"
						transition:fade={{ duration: 600, delay: 600 }}
					>
						We'll be right back :(
					</p>
				</div>

				{#if isDevelopment && data.error}
					<div
						class="mb-8 rounded-lg bg-destructive/10 p-4 text-left"
						transition:fade={{ duration: 400, delay: 900 }}
					>
						<p class="mb-2 font-mono text-sm text-destructive">
							<strong>Dev Error:</strong>
							{data.error instanceof Error ? data.error.message : String(data.error)}
						</p>
					</div>
				{/if}

				<div
					class="flex flex-col gap-3 sm:flex-row sm:justify-center"
					transition:fade={{ duration: 400, delay: 1200 }}
				>
					<Button href="/" variant="default">Go to Home</Button>
					<Button href="/" variant="outline">Try Again</Button>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.error-page-container {
		position: relative;
		min-height: 100vh;
		overflow: hidden;
		background: var(--background);
	}

	.gradient-background {
		position: fixed;
		inset: 0;
		background: linear-gradient(
			135deg,
			#667eea 0%,
			#764ba2 25%,
			#f093fb 50%,
			#4facfe 75%,
			#00f2fe 100%
		);
		background-size: 400% 400%;
		animation: gradient-wave 15s ease infinite;
		opacity: 0.15;
		z-index: 0;
	}

	.dark .gradient-background {
		opacity: 0.25;
	}

	@keyframes gradient-wave {
		0% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}

	.sparkles-container {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 1;
		overflow: hidden;
	}

	.sparkle {
		position: absolute;
		bottom: -20px;
		border-radius: 50%;
		background: radial-gradient(
			circle,
			rgba(255, 255, 255, 0.9) 0%,
			rgba(255, 215, 0, 0.8) 30%,
			rgba(255, 192, 203, 0.7) 60%,
			rgba(135, 206, 250, 0.6) 100%
		);
		box-shadow:
			0 0 15px rgba(255, 215, 0, 0.8),
			0 0 25px rgba(255, 192, 203, 0.6),
			0 0 35px rgba(135, 206, 250, 0.4),
			0 0 50px rgba(255, 255, 255, 0.3);
		animation: sparkle-rise linear infinite;
		filter: blur(0.5px);
	}

	@keyframes sparkle-rise {
		0% {
			transform: translateY(0) translateX(0) scale(0.3);
			opacity: 0;
			filter: blur(0.5px) brightness(0.5);
		}
		5% {
			opacity: 1;
			filter: blur(0.5px) brightness(1);
		}
		50% {
			transform: translateY(-50vh) translateX(calc(var(--drift, 0) * 50px)) scale(1);
			filter: blur(0.5px) brightness(1.5);
		}
		95% {
			opacity: 1;
			filter: blur(0.5px) brightness(1);
		}
		100% {
			transform: translateY(-100vh) translateX(calc(var(--drift, 0) * 100px)) scale(1.5);
			opacity: 0;
			filter: blur(1px) brightness(0.5);
		}
	}

	@keyframes shimmer {
		0% {
			background-position: -200% center;
		}
		100% {
			background-position: 200% center;
		}
	}

	.animate-shimmer {
		background-size: 200% auto;
		animation: shimmer 3s linear infinite;
	}
</style>
