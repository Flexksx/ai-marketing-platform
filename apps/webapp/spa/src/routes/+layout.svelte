<script lang="ts">
	import { invalidate } from '$app/navigation';
	import favicon from '$lib/assets/vozai_logo.png';
	import '$lib/axios-interceptor';
	import { navigate } from '$lib/navigation';
	import { theme } from '$lib/stores/theme';
	import { supabase } from '$lib/supabase/client';
	import { QueryClientProvider } from '@tanstack/svelte-query';
	import { onMount } from 'svelte';
	import '../app.css';

	let { data, children } = $props();

	onMount(() => {
		theme.init();

		const { data: subscriptionData } = supabase.auth.onAuthStateChange(async (event) => {
			if (event === 'SIGNED_OUT') {
				await invalidate('supabase:auth');
				navigate('/login');
				return;
			}
		});

		return () => subscriptionData.subscription.unsubscribe();
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<QueryClientProvider client={data.queryClient}>
	{@render children?.()}
</QueryClientProvider>
