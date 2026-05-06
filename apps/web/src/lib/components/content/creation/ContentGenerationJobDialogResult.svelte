<script lang="ts">
	import type { ContentGenerationJobResult } from '$lib/api/content-generation-jobs/ContentGenerationJobResult';
	import { useAcceptContentGenerationJob } from '$lib/api/content-generation-jobs/mutations';
	import ContentPreview from '$lib/components/content/ContentPreview.svelte';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import { Check } from '@lucide/svelte';

	type Brand = { id: string };

	type Props = {
		result: ContentGenerationJobResult | null;
		jobId: string | null;
		brand: Brand;
		onClose: () => void;
		onGenerateAnother: () => void;
	};

	let { result, jobId, brand, onClose, onGenerateAnother }: Props = $props();

	const acceptMutation = useAcceptContentGenerationJob();
	let acceptError = $state<string | null>(null);

	function handleAccept() {
		if (!jobId) return;
		acceptError = null;
		acceptMutation.mutate(
			{ brandId: brand.id, jobId },
			{
				onSuccess: onClose,
				onError: (err) => {
					acceptError = err instanceof Error ? err.message : 'Failed to accept content';
				}
			}
		);
	}
</script>

<div class="flex min-h-0 flex-1 flex-col gap-4 overflow-hidden">
	<div class="flex min-h-0 flex-1 flex-col gap-2 overflow-hidden">
		<Label class="shrink-0">Generated Content</Label>
		<div
			class="min-h-0 flex-1 overflow-x-hidden overflow-y-auto rounded-lg border bg-muted/30 p-4 min-w-0"
		>
			<ContentPreview {result} />
		</div>
	</div>

	{#if acceptError}
		<div class="shrink-0 text-sm text-destructive bg-destructive/10 p-3 rounded-lg">
			{acceptError}
		</div>
	{/if}

	<div class="flex shrink-0 gap-3 border-t pt-4">
		<Button variant="secondary" onclick={onGenerateAnother} class="flex-1">Generate Another</Button>
		<Button onclick={handleAccept} disabled={acceptMutation.isPending || !jobId} class="flex-1">
			<Check class="mr-2 h-4 w-4" />
			{acceptMutation.isPending ? 'Accepting...' : 'Accept & Schedule'}
		</Button>
	</div>
</div>
