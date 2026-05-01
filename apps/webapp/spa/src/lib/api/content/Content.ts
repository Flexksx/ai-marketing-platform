import type { ContentChannelName } from '../content-channel/ContentChannelName';
import {
	ContentData,
	TextOnlyContentData,
	TextWithSingleImageContentData,
	type ContentDataResponse
} from './ContentData';
import type { ContentFormat } from './ContentFormat';

export interface ContentResponse {
	id: string;
	brand_id: string;
	campaign_id: string | null;
	channel: ContentChannelName;
	content_format: ContentFormat;
	data: ContentDataResponse;
	scheduled_at: string | null;
	created_at: string;
	updated_at: string;
}

export class Content {
	constructor(
		public readonly id: string,
		public readonly brandId: string,
		public readonly campaignId: string | null,
		public readonly channel: ContentChannelName,
		public readonly contentFormat: ContentFormat,
		public readonly data: ContentData,
		public readonly scheduledAt: string | null,
		public readonly createdAt: string,
		public readonly updatedAt: string
	) {}

	get caption(): string {
		if (
			this.data instanceof TextOnlyContentData ||
			this.data instanceof TextWithSingleImageContentData
		) {
			return this.data.caption;
		}
		return '';
	}

	get mediaUrl(): string | null {
		if (this.data instanceof TextWithSingleImageContentData) {
			return this.data.imageUrl;
		}
		return null;
	}

	static fromResponse(response: ContentResponse): Content {
		return new Content(
			response.id,
			response.brand_id,
			response.campaign_id,
			response.channel,
			response.content_format,
			ContentData.fromResponse(response.data),
			response.scheduled_at,
			response.created_at,
			response.updated_at
		);
	}
}
