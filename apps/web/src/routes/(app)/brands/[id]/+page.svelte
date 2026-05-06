<script lang="ts">
	import { page } from '$app/state';
	import { navigate } from '$lib/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		navigate(`/brands/${page.params.id}/settings`);
	});
</script>
