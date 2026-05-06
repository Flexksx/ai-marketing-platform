import type { ContentChannelName } from '../content-channel/ContentChannelName';

export interface ContentListRequest {
	brand_id?: string | null;
	campaign_id?: string | null;
	channel?: ContentChannelName | null;
	scheduled_after?: string | null;
	scheduled_before?: string | null;
	limit?: number | null;
	offset?: number | null;
}
