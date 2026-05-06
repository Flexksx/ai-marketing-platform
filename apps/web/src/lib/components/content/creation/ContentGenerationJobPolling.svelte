<script lang="ts">
	import * as Empty from '$lib/components/ui/empty';
	import { Loader2 } from '@lucide/svelte';

	type Props = {
		message?: string;
	};

	let { message = 'Generating your content...' }: Props = $props();
</script>

<Empty.Root class="min-h-[240px] py-8">
	<Empty.Header>
		<Empty.Media variant="icon">
			<Loader2 class="h-6 w-6 animate-spin" />
		</Empty.Media>
		<Empty.Title>{message}</Empty.Title>
		<Empty.Description>
			This may take a moment. You can close the dialog and we'll keep generating in the background.
		</Empty.Description>
	</Empty.Header>
</Empty.Root>
