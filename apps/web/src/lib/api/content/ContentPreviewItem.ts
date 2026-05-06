import type { ContentChannelName } from '../content-channel/ContentChannelName';

export interface ContentPreviewItem {
	caption: string | null;
	mediaUrl: string | null;
	channel: ContentChannelName;
	scheduledAt: string | null;
}
