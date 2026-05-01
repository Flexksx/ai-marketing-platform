<script lang="ts">
	import type { ContentGenerationJobDialogState } from '$lib/components/content/creation/content-generation-job-dialog-state';
	import { Button } from '$lib/components/ui/button';
	import { Check, Loader2, Megaphone, Sparkles } from '@lucide/svelte';

	type CalendarToolbarProps = {
		onCreateCampaign: () => void;
		onCreateContent: () => void;
		contentJobState?: ContentGenerationJobDialogState;
	};

	let {
		onCreateCampaign,
		onCreateContent,
		contentJobState = 'idle'
	}: CalendarToolbarProps = $props();
</script>

<div class="fixed bottom-8 left-0 right-0 z-10 flex justify-center py-4">
	<div
		class="bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border rounded-full px-6 py-3 shadow-lg"
	>
		<div class="flex items-center gap-3">
			<Button
				onclick={onCreateCampaign}
				variant="default"
				class="gap-2 btn-rounded-full border-none"
				size="default"
			>
				<Sparkles class="h-5 w-5" />
				New Content Plan
			</Button>
			<Button
				onclick={onCreateContent}
				variant="secondary"
				class="gap-2 btn-rounded-full border-none"
				size="default"
			>
				{#if contentJobState === 'polling'}
					<Loader2 class="h-5 w-5 animate-spin" />
				{:else if contentJobState === 'complete'}
					<Check class="h-5 w-5" />
				{:else}
					<Megaphone class="h-5 w-5" />
				{/if}
				New Content
			</Button>
		</div>
	</div>
</div>
