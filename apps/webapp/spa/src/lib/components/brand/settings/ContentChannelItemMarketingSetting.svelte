<script lang="ts">
	import type { ContentChannelName } from '$lib/api/generated/models/ContentChannelName';

	interface ContentChannelBrandMarketingSetting {
		channel_name: ContentChannelName;
		hashtag_level: number;
		emoji_level: number;
	}
	import ChannelLevelSlider from '$lib/components/brand/settings/ChannelLevelSlider.svelte';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Label } from '$lib/components/ui/label';
	import { Instagram, Linkedin } from 'lucide-svelte';

	interface Props {
		channel: ContentChannelBrandMarketingSetting;
		readonly?: boolean;
	}

	let { channel, readonly = false }: Props = $props();

	const ChannelIcon = $derived(
		channel.channel_name === 'INSTAGRAM' ? Instagram : Linkedin
	);
</script>

<Card class="border bg-card rounded-xl overflow-hidden">
	<CardHeader class="flex flex-row items-center gap-2 space-y-0 pb-2">
		<ChannelIcon class="size-5 shrink-0 text-muted-foreground" />
		<CardTitle class="text-base">{channel.channel_name}</CardTitle>
	</CardHeader>
	<CardContent class="pt-0">
		<div class="flex flex-wrap items-end gap-6">
			<div class="space-y-1.5 min-w-[200px]">
				<Label class="text-xs text-muted-foreground">Hashtag level</Label>
				<ChannelLevelSlider
					bind:value={channel.hashtag_level}
					type="hashtag"
					disabled={readonly}
				/>
			</div>
			<div class="space-y-1.5 min-w-[200px]">
				<Label class="text-xs text-muted-foreground">Emoji level</Label>
				<ChannelLevelSlider
					bind:value={channel.emoji_level}
					type="emoji"
					disabled={readonly}
				/>
			</div>
		</div>
	</CardContent>
</Card>
