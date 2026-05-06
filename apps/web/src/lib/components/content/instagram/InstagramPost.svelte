<script lang="ts">
	import type { Content } from '$lib/api/content/Content';
	import { Heart, MessageCircle, Send, Bookmark, MoreHorizontal } from 'lucide-svelte';

	type Props = {
		post: Content;
	};

	let { post }: Props = $props();

	const formatInstagramDate = (dateString: string | null): string => {
		if (!dateString) return '';
		try {
			const date = new Date(dateString);
			const now = new Date();
			const diffMs = now.getTime() - date.getTime();
			const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
			const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

			if (diffHours < 1) return 'just now';
			if (diffHours < 24) return `${diffHours}h`;
			if (diffDays < 7) return `${diffDays}d`;
			return `${Math.floor(diffDays / 7)}w`;
		} catch {
			return '';
		}
	};

	const hashtags = $derived.by(() => {
		const matches = post.caption.match(/#\w+/g);
		return matches || [];
	});

	const captionWithoutExcessHashtags = $derived.by(() => {
		const lines = post.caption.split('\n');
		const mainText: string[] = [];

		for (const line of lines) {
			const hashtagCount = (line.match(/#/g) || []).length;
			if (hashtagCount <= 2) {
				mainText.push(line);
			}
		}

		return mainText.join('\n');
	});
</script>

<div class="bg-white border border-slate-200 rounded-lg overflow-hidden max-w-md mx-auto shadow-sm">
	<div class="flex items-center justify-between px-3 py-2.5">
		<div class="flex items-center gap-2.5">
			<div
				class="w-8 h-8 rounded-full bg-gradient-to-tr from-yellow-400 via-pink-500 to-purple-600 p-0.5"
			>
				<div class="w-full h-full rounded-full bg-white flex items-center justify-center">
					<div class="w-6 h-6 rounded-full bg-slate-200"></div>
				</div>
			</div>
			<div class="flex flex-col">
				<span class="text-sm font-semibold !text-slate-900">your_brand</span>
			</div>
		</div>
		<button class="text-slate-900">
			<MoreHorizontal class="w-6 h-6" />
		</button>
	</div>

	{#if post.mediaUrl}
		<div class="w-full aspect-square bg-slate-100">
			<img src={post.mediaUrl} alt="Content" class="w-full h-full object-cover" />
		</div>
	{/if}

	<div class="px-3 py-2">
		<div class="flex items-center justify-between mb-2">
			<div class="flex items-center gap-4">
				<button class="!text-slate-900 hover:!text-slate-600 transition-colors">
					<Heart class="w-6 h-6" />
				</button>
				<button class="!text-slate-900 hover:!text-slate-600 transition-colors">
					<MessageCircle class="w-6 h-6" />
				</button>
				<button class="!text-slate-900 hover:!text-slate-600 transition-colors">
					<Send class="w-6 h-6" />
				</button>
			</div>
			<button class="!text-slate-900 hover:!text-slate-600 transition-colors">
				<Bookmark class="w-6 h-6" />
			</button>
		</div>

		<div class="text-sm font-semibold mb-1 !text-slate-900">1,234 likes</div>

		{#if post.caption}
			<div class="text-sm !text-slate-900">
				<span class="font-semibold">your_brand</span>
				<span class="ml-1 whitespace-pre-wrap">{captionWithoutExcessHashtags}</span>
			</div>

			{#if hashtags.length > 0}
				<div class="text-sm mt-1 !text-blue-900">
					{hashtags.slice(0, 5).join(' ')}
				</div>
			{/if}
		{/if}

		{#if post.scheduledAt}
			<div class="text-xs !text-slate-400 uppercase mt-2">
				{formatInstagramDate(post.scheduledAt)}
			</div>
		{/if}
	</div>
</div>
