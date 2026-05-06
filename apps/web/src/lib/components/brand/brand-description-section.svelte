<script lang="ts">
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Edit3 } from '@lucide/svelte';
	import MarkdownRenderer from '$lib/components/ui/markdown-renderer.svelte';
	import type { LucideIcon } from '@lucide/svelte';

	type Props = {
		title: string;
		content: string;
		icon: LucideIcon;
		iconColor?: 'blue' | 'green' | 'purple' | 'orange';
		editable?: boolean;
		onEdit?: () => void;
	};

	let {
		title,
		content,
		icon: Icon,
		iconColor = 'blue',
		editable = true,
		onEdit
	}: Props = $props();

	const iconColorClasses = {
		blue: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
		green: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
		purple: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
		orange: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400'
	};
</script>

<Card
	class="group cursor-pointer border-0 bg-white/80 shadow-xl backdrop-blur-sm transition-all hover:-translate-y-1 hover:shadow-2xl dark:bg-slate-800/80"
	onclick={() => editable && onEdit?.()}
>
	<CardContent class="p-8">
		<div class="mb-6 flex items-start justify-between">
			<div class="flex items-center gap-3">
				<div class="rounded-lg p-2 {iconColorClasses[iconColor]}">
					<Icon class="h-5 w-5" />
				</div>
				<h3 class="text-xl font-semibold">{title}</h3>
			</div>
			{#if editable}
				<Edit3
					class="h-5 w-5 text-slate-400 opacity-0 transition-opacity group-hover:opacity-100"
				/>
			{/if}
		</div>
		<div class="max-w-5xl">
			<MarkdownRenderer content={content || 'No description yet...'} />
		</div>
	</CardContent>
</Card>

