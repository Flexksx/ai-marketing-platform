import type { ContentData } from './ContentData';
import type { ContentChannelName } from '../content-channel/ContentChannelName';
import type { ContentFormat } from './ContentFormat';

export interface ContentUpdateRequest {
	channel?: ContentChannelName | null;
	content_format?: ContentFormat | null;
	data?: ContentData | null;
	scheduled_at?: string | null;
}
