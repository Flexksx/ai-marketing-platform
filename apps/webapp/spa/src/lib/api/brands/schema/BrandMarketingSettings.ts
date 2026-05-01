import type { ContentChannelBrandMarketingSetting } from './ContentChannelBrandMarketingSetting';

export interface BrandMarketingSettings {
	content_pillars: string[];
	content_channels: ContentChannelBrandMarketingSetting[];
}
