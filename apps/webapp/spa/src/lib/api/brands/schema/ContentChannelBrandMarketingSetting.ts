import type { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';

export interface ContentChannelBrandMarketingSetting {
	channel_name: ContentChannelName;
	hashtag_level: number;
	emoji_level: number;
}
