<script lang="ts">
	import { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';
	import type { ContentGenerationJobResult } from '$lib/api/content-generation-jobs/ContentGenerationJobResult';
	import { Content } from '$lib/api/content/Content';
	import InstagramPost from '$lib/components/content/instagram/InstagramPost.svelte';
	import LinkedInPost from '$lib/components/content/linkedin/LinkedInPost.svelte';
	import { ImageIcon } from '@lucide/svelte';

	type Props = {
		result: ContentGenerationJobResult | null;
	};

	let { result }: Props = $props();

	const mappedContent = $derived.by((): Content | null => {
		if (!result || !result.data) return null;

		const data = result.data;
		const scheduledAt = result.scheduledAt.toISOString();

		return new Content(
			'preview',
			'preview-brand',
			'preview-campaign',
			result.channel,
			data.contentFormat,
			data,
			scheduledAt,
			new Date().toISOString(),
			new Date().toISOString()
		);
	});
</script>

<div class="w-full h-full flex items-center justify-center">
	{#if result && mappedContent}
		<div class="w-full max-w-md">
			{#if result.channel === ContentChannelName.INSTAGRAM}
				<InstagramPost post={mappedContent} />
			{:else if result.channel === ContentChannelName.LINKEDIN}
				<LinkedInPost post={mappedContent} />
			{/if}
		</div>
	{:else}
		<div class="flex flex-col items-center justify-center gap-4 text-muted-foreground py-12">
			<div class="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center">
				<ImageIcon class="h-8 w-8 text-slate-400" />
			</div>
			<div class="text-center">
				<p class="text-sm font-medium">No preview available</p>
				<p class="text-xs mt-1">Content will appear here after generation</p>
			</div>
		</div>
	{/if}
</div>
