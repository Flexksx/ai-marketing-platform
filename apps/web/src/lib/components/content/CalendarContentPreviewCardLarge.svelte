<script lang="ts">
	import type { ContentPreviewItem } from '$lib/api/content/ContentPreviewItem';
	import type { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';
	import instagramLogo from '$lib/assets/instagram_logo.png';
	import linkedinLogo from '$lib/assets/linkedin_logo.png';
	import { Card, CardContent } from '$lib/components/ui/card';

	type Props = {
		post: ContentPreviewItem;
		viewMode: 'week' | 'month';
		onclick?: () => void;
	};

	let { post, viewMode, onclick }: Props = $props();

	const getChannelLogo = (channel: ContentChannelName): string => {
		switch (channel) {
			case 'INSTAGRAM':
				return instagramLogo;
			case 'LINKEDIN':
				return linkedinLogo;
			default:
				return '';
		}
	};

	const formatTime = (scheduledAt: string | null): string => {
		if (!scheduledAt) return '';
		try {
			const date = new Date(scheduledAt);
			return date.toLocaleTimeString('en-US', {
				hour: '2-digit',
				minute: '2-digit',
				hour12: false
			});
		} catch {
			return '';
		}
	};

	const scheduledTime = $derived(formatTime(post.scheduledAt));

	const backgroundImageStyle = $derived(
		post.mediaUrl ? `background-image: url('${post.mediaUrl}');` : ''
	);

	const isWeekView = $derived(viewMode === 'week');
</script>

{#if isWeekView}
	<Card
		class="py-0 transition-shadow hover:shadow-lg cursor-pointer overflow-hidden h-[240px]"
		{onclick}
		role="button"
		tabindex={0}
		onkeydown={(e) => {
			if (e.key === 'Enter' || e.key === ' ') {
				e.preventDefault();
				onclick?.();
			}
		}}
	>
		<CardContent class="p-0 h-full relative">
			{#if post.mediaUrl}
				<div class="absolute inset-0 bg-cover bg-center" style={backgroundImageStyle}>
					<div
						class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/50 to-transparent"
					></div>
				</div>
			{:else}
				<div class="absolute inset-0 bg-muted"></div>
			{/if}
			<div class="relative h-full flex flex-col justify-between px-3">
				<div class="flex items-start justify-between py-3">
					<img
						src={getChannelLogo(post.channel)}
						alt={post.channel}
						draggable="false"
						class="h-5 w-5 drop-shadow-lg"
					/>
					{#if scheduledTime}
						<span class="text-white text-sm font-semibold drop-shadow-lg">{scheduledTime}</span>
					{/if}
				</div>
				<div class="pb-3">
					<p
						class="line-clamp-2 text-sm font-medium text-white drop-shadow-lg overflow-hidden break-words"
					>
						{post.caption || 'No caption'}
					</p>
				</div>
			</div>
		</CardContent>
	</Card>
{:else}
	<div
		class="rounded overflow-hidden hover:shadow-md transition-shadow cursor-pointer h-[90px] relative"
		{onclick}
		role="button"
		tabindex={0}
		onkeydown={(e) => {
			if (e.key === 'Enter' || e.key === ' ') {
				e.preventDefault();
				onclick?.();
			}
		}}
	>
		{#if post.mediaUrl}
			<div class="absolute inset-0 bg-cover bg-center" style={backgroundImageStyle}>
				<div
					class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/50 to-transparent"
				></div>
			</div>
		{:else}
			<div class="absolute inset-0 bg-muted"></div>
		{/if}
		<div class="relative h-full flex flex-col justify-between px-1.5">
			<div class="flex items-start justify-between py-1.5">
				<img
					src={getChannelLogo(post.channel)}
					alt={post.channel}
					draggable="false"
					class="h-3 w-3 drop-shadow-lg"
				/>
				{#if scheduledTime}
					<span class="text-white text-[10px] font-semibold drop-shadow-lg">{scheduledTime}</span>
				{/if}
			</div>
			<div class="pb-1.5">
				<p
					class="line-clamp-2 text-[10px] font-medium text-white drop-shadow-lg overflow-hidden break-words"
				>
					{post.caption || 'No caption'}
				</p>
			</div>
		</div>
	</div>
{/if}
