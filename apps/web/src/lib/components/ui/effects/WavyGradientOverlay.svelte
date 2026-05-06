<script lang="ts">
	import { Loader2 } from '@lucide/svelte';

	type Props = {
		show: boolean;
	};

	let { show = false }: Props = $props();
</script>

{#if show}
	<div
		class="absolute inset-0 z-50 flex items-center justify-center rounded-lg overflow-hidden"
		style="backdrop-filter: blur(8px);"
	>
		<div class="absolute inset-0 wavy-gradient opacity-90"></div>
		<div class="relative z-10 flex flex-col items-center gap-4 text-white">
			<Loader2 class="h-12 w-12 animate-spin" />
			<p class="text-lg font-semibold">AI is generating your content...</p>
			<p class="text-sm opacity-80">This may take a moment</p>
		</div>
	</div>
{/if}

<style>
	.wavy-gradient {
		background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
		background-size: 400% 400%;
		animation: wave 15s ease infinite;
	}

	@keyframes wave {
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
</style>
