<script lang="ts">
	import type { ContentGenerationJobResult } from '$lib/api/content-generation-jobs/ContentGenerationJobResult';
	import ContentGenerationJobDialogInputs from '$lib/components/content/creation/ContentGenerationJobDialogInputs.svelte';
	import ContentGenerationJobDialogResult from '$lib/components/content/creation/ContentGenerationJobDialogResult.svelte';
	import ContentGenerationJobPolling from '$lib/components/content/creation/ContentGenerationJobPolling.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Megaphone } from '@lucide/svelte';

	type Brand = { id: string };

	type Props = {
		brand: Brand;
		open?: boolean;
		contentGenerationJobId?: string | null;
		jobResult?: ContentGenerationJobResult | null;
		isPolling?: boolean;
		isComplete?: boolean;
		isFailed?: boolean;
	};

	let {
		brand,
		open = $bindable(false),
		contentGenerationJobId = $bindable(null),
		jobResult = null,
		isPolling = false,
		isComplete = false,
		isFailed = false
	}: Props = $props();

	function handleClose() {
		open = false;
		contentGenerationJobId = null;
	}

	function handleGenerateAnother() {
		contentGenerationJobId = null;
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Content
		class="flex h-[85vh] max-h-[85vh] w-max min-w-0 max-w-[calc(100vw-2rem)] flex-col overflow-hidden lg:min-w-[42rem]"
	>
		<Dialog.Header class="shrink-0">
			<Dialog.Title class="flex items-center gap-2">
				<Megaphone class="h-5 w-5 text-primary" />
				Create New Content
			</Dialog.Title>
			<Dialog.Description>
				Generate a single social media post with AI. Describe what you want to create, choose a
				channel, and schedule it.
			</Dialog.Description>
		</Dialog.Header>

		<div class="relative flex min-h-0 flex-1 flex-col overflow-y-auto py-4 min-w-0">
			{#if !contentGenerationJobId}
				<ContentGenerationJobDialogInputs
					{brand}
					onJobCreated={(id) => (contentGenerationJobId = id)}
				/>
			{:else if isPolling}
				<ContentGenerationJobPolling />
			{:else if isComplete}
				<ContentGenerationJobDialogResult
					result={jobResult}
					jobId={contentGenerationJobId}
					{brand}
					onClose={handleClose}
					onGenerateAnother={handleGenerateAnother}
				/>
			{:else if isFailed}
				<div class="flex flex-col gap-4 py-4">
					<div class="text-sm text-destructive bg-destructive/10 p-3 rounded-lg">
						Content generation failed. Please try again.
					</div>
					<Button variant="outline" onclick={handleGenerateAnother} class="w-full">
						Try again
					</Button>
				</div>
			{/if}
		</div>
	</Dialog.Content>
</Dialog.Root>
