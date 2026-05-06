<script lang="ts">
	import type { Content } from '$lib/api/content/Content';
	import { Globe, ThumbsUp, MessageSquare, Repeat2, Send, MoreHorizontal } from 'lucide-svelte';

	type Props = {
		post: Content;
	};

	let { post }: Props = $props();

	const isLongCaption = $derived(post.caption && post.caption.length > 300);

	const formatLinkedInDate = (dateString: string | null): string => {
		if (!dateString) return '';
		try {
			const date = new Date(dateString);
			const now = new Date();
			const diffMs = now.getTime() - date.getTime();
			const diffMinutes = Math.floor(diffMs / (1000 * 60));
			const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
			const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
			const diffWeeks = Math.floor(diffDays / 7);
			const diffMonths = Math.floor(diffDays / 30);

			if (diffMinutes < 1) return 'Just now';
			if (diffMinutes < 60) return `${diffMinutes}m`;
			if (diffHours < 24) return `${diffHours}h`;
			if (diffDays < 7) return `${diffDays}d`;
			if (diffWeeks < 4) return `${diffWeeks}w`;
			return `${diffMonths}mo`;
		} catch {
			return '';
		}
	};
</script>

<div class="bg-white border border-slate-300 rounded-lg overflow-hidden max-w-xl mx-auto shadow-sm">
	<div class="p-3">
		<div class="flex items-start justify-between mb-2">
			<div class="flex gap-2">
				<div class="w-12 h-12 rounded-full bg-slate-200 flex-shrink-0"></div>
				<div class="flex flex-col">
					<span class="text-sm font-semibold !text-slate-900">Your Company</span>
					<span class="text-xs !text-slate-600">Company tagline</span>
					<div class="flex items-center gap-1 text-xs !text-slate-500 mt-0.5">
						{#if post.scheduledAt}
							<span>{formatLinkedInDate(post.scheduledAt)}</span>
							<span>•</span>
						{/if}
						<Globe class="w-3 h-3" />
					</div>
				</div>
			</div>
			<button class="!text-slate-600 hover:!bg-slate-100 rounded p-1">
				<MoreHorizontal class="w-5 h-5" />
			</button>
		</div>

		{#if post.caption}
			<div
				class="!text-slate-900 mb-3 whitespace-pre-wrap leading-relaxed"
				class:text-xs={isLongCaption}
				class:text-sm={!isLongCaption}
			>
				{post.caption}
			</div>
		{/if}
	</div>

	{#if post.mediaUrl}
		<div class="w-full bg-slate-100">
			<img src={post.mediaUrl} alt="Post content" class="w-full h-auto object-cover" />
		</div>
	{/if}

	<div class="px-3 py-2 border-t border-slate-200">
		<div class="flex items-center justify-between text-xs !text-slate-600 mb-2">
			<div class="flex items-center gap-1">
				<div class="flex -space-x-1">
					<div class="w-4 h-4 rounded-full bg-blue-500 flex items-center justify-center">
						<ThumbsUp class="w-2.5 h-2.5 text-white fill-white" />
					</div>
				</div>
				<span>47 reactions</span>
			</div>
			<div class="flex items-center gap-2">
				<span>12 comments</span>
				<span>•</span>
				<span>3 reposts</span>
			</div>
		</div>

		<div class="border-t border-slate-200 pt-1">
			<div class="flex items-center justify-around">
				<button
					class="flex items-center gap-2 px-4 py-2 !text-slate-600 hover:!bg-slate-100 rounded transition-colors"
				>
					<ThumbsUp class="w-5 h-5" />
					<span class="text-sm font-semibold">Like</span>
				</button>
				<button
					class="flex items-center gap-2 px-4 py-2 !text-slate-600 hover:!bg-slate-100 rounded transition-colors"
				>
					<MessageSquare class="w-5 h-5" />
					<span class="text-sm font-semibold">Comment</span>
				</button>
				<button
					class="flex items-center gap-2 px-4 py-2 !text-slate-600 hover:!bg-slate-100 rounded transition-colors"
				>
					<Repeat2 class="w-5 h-5" />
					<span class="text-sm font-semibold">Repost</span>
				</button>
				<button
					class="flex items-center gap-2 px-4 py-2 !text-slate-600 hover:!bg-slate-100 rounded transition-colors"
				>
					<Send class="w-5 h-5" />
					<span class="text-sm font-semibold">Send</span>
				</button>
			</div>
		</div>
	</div>
</div>
