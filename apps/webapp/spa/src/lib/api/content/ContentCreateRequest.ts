import type { ContentChannelName } from '../content-channel/ContentChannelName';
import type { ContentData } from './ContentData';
import type { ContentFormat } from './ContentFormat';

export interface ContentCreateRequest {
	brand_id: string;
	campaign_id: string | null;
	channel: ContentChannelName;
	content_format: ContentFormat;
	data: ContentData;
	scheduled_at: string;
}
