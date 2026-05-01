<script lang="ts">
	import { beforeNavigate } from '$app/navigation';
	import { page } from '$app/state';
	import { SidebarProvider, SidebarInset } from '$lib/components/ui/sidebar';
	import BrandSidebar from '$lib/components/ui/vozai/sidebar/BrandSidebar.svelte';
	import type { Snippet } from 'svelte';

	type Props = {
		children: Snippet;
	};

	let { children }: Props = $props();

	const brandId = $derived(page.params.id);

	beforeNavigate(({ from, to }) => {
		if (
			!to ||
			!from?.url.pathname.includes('posts_calendar') ||
			from.url.searchParams.get('onboarded') !== 'true'
		) {
			return;
		}
		if (to.url.pathname.includes('posts_calendar')) {
			return;
		}
		const url = new URL(from.url);
		url.searchParams.delete('onboarded');
		const cleanPath = url.pathname + (url.search ? `?${url.search}` : '');
		history.replaceState(history.state, '', cleanPath);
	});
</script>

<SidebarProvider>
	<BrandSidebar selectedBrandId={brandId} />
	<SidebarInset class="flex h-screen flex-col">
		{@render children()}
	</SidebarInset>
</SidebarProvider>
