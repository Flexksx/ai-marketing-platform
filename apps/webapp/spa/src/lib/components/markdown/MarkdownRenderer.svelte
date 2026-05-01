<script lang="ts">
	import { marked } from 'marked';

	type Props = {
		content: string;
		class?: string;
	};

	let { content, class: className = '' }: Props = $props();

	// Configure marked options
	marked.setOptions({
		breaks: true,
		gfm: true,
		headerIds: false,
		mangle: false
	});

	let htmlContent = $derived.by(() => {
		if (!content || typeof content !== 'string') {
			return '';
		}
		const trimmed = content.trim();
		if (!trimmed) {
			return '';
		}
		try {
			const parsed = marked.parse(trimmed) as string;
			return parsed;
		} catch (error) {
			return '';
		}
	});
</script>

{#if htmlContent}
	<div class="markdown-content {className}">
		{@html htmlContent}
	</div>
{:else if content && content.trim()}
	<p class="text-muted-foreground italic">No description yet...</p>
{/if}

<style>
	.markdown-content {
		max-width: none;
		color: rgb(51 65 85);
		line-height: 1.75;
	}

	:global(.dark) .markdown-content {
		color: rgb(203 213 225);
	}

	.markdown-content :global(p) {
		margin-top: 1rem;
		margin-bottom: 1rem;
	}

	.markdown-content :global(strong) {
		font-weight: 600;
		color: inherit;
	}

	.markdown-content :global(h1),
	.markdown-content :global(h2),
	.markdown-content :global(h3),
	.markdown-content :global(h4),
	.markdown-content :global(h5),
	.markdown-content :global(h6) {
		font-weight: 600;
		margin-top: 1.5rem;
		margin-bottom: 0.75rem;
		line-height: 1.25;
		color: inherit;
	}

	.markdown-content :global(h1) {
		font-size: 2.25rem;
		margin-top: 0;
	}

	.markdown-content :global(h2) {
		font-size: 1.875rem;
	}

	.markdown-content :global(h3) {
		font-size: 1.5rem;
	}

	.markdown-content :global(h4) {
		font-size: 1.25rem;
	}

	.markdown-content :global(ul),
	.markdown-content :global(ol) {
		margin-top: 1rem;
		margin-bottom: 1rem;
		padding-left: 1.5rem;
	}

	.markdown-content :global(ul) {
		list-style-type: disc;
	}

	.markdown-content :global(ol) {
		list-style-type: decimal;
	}

	.markdown-content :global(li) {
		margin-top: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.markdown-content :global(ul > li),
	.markdown-content :global(ol > li) {
		padding-left: 0.375rem;
	}

	.markdown-content :global(ul > li::marker),
	.markdown-content :global(ol > li::marker) {
		color: rgb(100 116 139);
	}

	:global(.dark) .markdown-content :global(ul > li::marker),
	:global(.dark) .markdown-content :global(ol > li::marker) {
		color: rgb(148 163 184);
	}

	.markdown-content :global(blockquote) {
		border-left: 4px solid rgb(226 232 240);
		padding-left: 1rem;
		margin: 1.5rem 0;
		font-style: italic;
		color: rgb(100 116 139);
	}

	:global(.dark) .markdown-content :global(blockquote) {
		border-left-color: rgb(51 65 85);
		color: rgb(148 163 184);
	}

	.markdown-content :global(code) {
		background-color: rgb(241 245 249);
		padding: 0.125rem 0.375rem;
		border-radius: 0.25rem;
		font-size: 0.875em;
		font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
	}

	:global(.dark) .markdown-content :global(code) {
		background-color: rgb(30 41 59);
	}

	.markdown-content :global(pre) {
		background-color: rgb(241 245 249);
		padding: 1rem;
		border-radius: 0.5rem;
		overflow-x: auto;
		margin: 1.5rem 0;
	}

	:global(.dark) .markdown-content :global(pre) {
		background-color: rgb(30 41 59);
	}

	.markdown-content :global(pre code) {
		background-color: transparent;
		padding: 0;
	}

	.markdown-content :global(a) {
		color: rgb(59 130 246);
		text-decoration: underline;
	}

	.markdown-content :global(a:hover) {
		color: rgb(37 99 235);
	}

	:global(.dark) .markdown-content :global(a) {
		color: rgb(96 165 250);
	}

	:global(.dark) .markdown-content :global(a:hover) {
		color: rgb(147 197 253);
	}
</style>
