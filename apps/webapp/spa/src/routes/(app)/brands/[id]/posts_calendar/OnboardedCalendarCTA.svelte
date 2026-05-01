<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Megaphone, Sparkles } from '@lucide/svelte';

	type Props = {
		onCreateCampaign: () => void;
		onCreateContent: () => void;
	};

	let { onCreateCampaign, onCreateContent }: Props = $props();
</script>

<div class="fixed inset-0 z-10 flex items-center justify-center pointer-events-none">
	<div class="pointer-events-auto flex flex-col sm:flex-row gap-4 md:gap-6 p-4">
		<Card
			class="w-full sm:w-64 md:w-72 cursor-pointer transition-all hover:scale-[1.02] hover:shadow-lg border-2 hover:border-accent"
			role="button"
			tabindex="0"
			onclick={onCreateCampaign}
			onkeydown={(e) => e.key === 'Enter' && onCreateCampaign()}
		>
			<CardContent class="p-6 flex flex-col items-center gap-3">
				<div class="rounded-full bg-accent/20 p-4">
					<Sparkles class="h-8 w-8 text-accent" />
				</div>
				<Button
					variant="default"
					size="lg"
					class="w-full btn-rounded-full bg-accent text-accent-foreground hover:bg-accent/90"
				>
					Create Content Plan
				</Button>
			</CardContent>
		</Card>
		<Card
			class="w-full sm:w-64 md:w-72 cursor-pointer transition-all hover:scale-[1.02] hover:shadow-lg border-2 hover:border-secondary"
			role="button"
			tabindex="0"
			onclick={onCreateContent}
			onkeydown={(e) => e.key === 'Enter' && onCreateContent()}
		>
			<CardContent class="p-6 flex flex-col items-center gap-3">
				<div class="rounded-full bg-secondary p-4">
					<Megaphone class="h-8 w-8 text-secondary-foreground" />
				</div>
				<Button variant="secondary" size="lg" class="w-full btn-rounded-full">
					Create Single Content
				</Button>
			</CardContent>
		</Card>
	</div>
</div>
