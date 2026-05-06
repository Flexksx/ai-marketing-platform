<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Trash2 } from 'lucide-svelte';

	type Props = {
		onDeleteClick: () => void;
	};

	let { onDeleteClick }: Props = $props();
</script>

<Card class="border-red-200">
	<CardHeader>
		<CardTitle class="text-red-600">Danger Zone</CardTitle>
	</CardHeader>
	<CardContent class="flex justify-between items-center">
		<p class="text-muted-foreground">Permanently delete this brand and all its data.</p>
		<Button variant="destructive" onclick={onDeleteClick}>
			<Trash2 class="mr-2 h-4 w-4" /> Delete Brand
		</Button>
	</CardContent>
</Card>
