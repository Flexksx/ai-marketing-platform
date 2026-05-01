<script lang="ts">
	import { resolve } from '$app/paths';
	import { useStartBrandGenerationJob } from '$lib/api/brand-generation-jobs/mutations';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { navigate } from '$lib/navigation';
	import { ArrowRight } from '@lucide/svelte';

	type Props = {
		disabled?: boolean;
	};

	let { disabled = false }: Props = $props();

	const createJobMutation = useStartBrandGenerationJob();

	let websiteUrl = $state('');
	let error = $state<string | null>(null);

	function normalizeWebsiteUrl(value: string): string {
		const trimmed = value.trim();
		if (!trimmed) return '';
		if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) return trimmed;
		if (trimmed.startsWith('//')) return `https:${trimmed}`;
		return `https://${trimmed}`;
	}

	function validate(): string | null {
		const normalized = normalizeWebsiteUrl(websiteUrl);
		if (!normalized) return 'Please enter a website URL';
		try {
			new URL(normalized);
		} catch {
			return 'Please enter a valid URL';
		}
		return null;
	}

	function handleSubmit() {
		const validationError = validate();
		if (validationError) {
			error = validationError;
			return;
		}
		error = null;

		const normalized = normalizeWebsiteUrl(websiteUrl);
		websiteUrl = normalized;

		createJobMutation.mutate(
			{ website_url: normalized },
			{
				onSuccess: (job) => {
					navigate(resolve(`/brands/create/${job.id}`));
				},
				onError: (err) => {
					error = err instanceof Error ? err.message : 'Failed to start brand extraction';
				}
			}
		);
	}
</script>

<div class="w-full max-w-2xl space-y-6">
	<div class="text-center space-y-2">
		<h1 class="text-4xl md:text-5xl font-bold mb-4 text-foreground">Create Your Brand</h1>
		<p class="text-lg text-muted-foreground" style="font-family: var(--font-body);">
			Enter your website URL and we'll extract your brand identity
		</p>
	</div>

	<form
		onsubmit={(e) => {
			e.preventDefault();
			handleSubmit();
		}}
		class="space-y-4"
	>
		<div class="relative">
			<Input
				type="text"
				inputmode="url"
				autocomplete="url"
				bind:value={websiteUrl}
				placeholder="https://"
				class="h-16 text-lg pr-16 border-2 focus:border-primary rounded-xl"
				disabled={disabled || createJobMutation.isPending}
			/>
			<Button
				type="submit"
				size="icon"
				class="absolute right-2 top-1/2 -translate-y-1/2 h-12 w-12 rounded-lg"
				disabled={disabled || createJobMutation.isPending || !websiteUrl.trim()}
			>
				<ArrowRight class="h-5 w-5" />
			</Button>
		</div>

		{#if error}
			<div class="text-sm text-destructive text-center bg-destructive/10 p-3 rounded-lg">
				{error}
			</div>
		{/if}
	</form>
</div>
