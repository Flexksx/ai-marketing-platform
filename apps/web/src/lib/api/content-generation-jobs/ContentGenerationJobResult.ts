import type { ContentChannelName } from '../content-channel/ContentChannelName';
import {
	TextOnlyContentData,
	TextWithSingleImageContentData,
	type TextOnlyContentDataResponse,
	type TextWithSingleImageContentDataResponse
} from '../content/ContentData';
import { ContentFormat } from '../content/ContentFormat';

export interface BaseContentGenerationJobResultResponse {
	channel: ContentChannelName;
	scheduled_at: string;
}

export interface TextWithSingleImageContentGenerationJobResultResponse
	extends BaseContentGenerationJobResultResponse {
	data: TextWithSingleImageContentDataResponse;
}

export interface TextOnlyContentGenerationJobResultResponse
	extends BaseContentGenerationJobResultResponse {
	data: TextOnlyContentDataResponse;
}

export type ContentGenerationJobResultResponse =
	| TextWithSingleImageContentGenerationJobResultResponse
	| TextOnlyContentGenerationJobResultResponse;

export abstract class ContentGenerationJobResult {
	constructor(
		public readonly channel: ContentChannelName,
		public readonly scheduledAt: Date
	) {}
	static fromResponse(response: ContentGenerationJobResultResponse) {
		switch (response.data.content_format) {
			case ContentFormat.TEXT_WITH_SINGLE_IMAGE:
				return TextWithSingleImageContentGenerationJobResult.fromResponse(
					response as TextWithSingleImageContentGenerationJobResultResponse
				);
			case ContentFormat.TEXT:
				return TextOnlyContentGenerationJobResult.fromResponse(
					response as TextOnlyContentGenerationJobResultResponse
				);
			default:
				throw new Error(`Unknown content format: ${response}`);
		}
	}
}

export class TextWithSingleImageContentGenerationJobResult extends ContentGenerationJobResult {
	constructor(
		public readonly channel: ContentChannelName,
		public readonly scheduledAt: Date,
		public readonly data: TextWithSingleImageContentData
	) {
		super(channel, scheduledAt);
	}
	static fromResponse(response: TextWithSingleImageContentGenerationJobResultResponse) {
		return new TextWithSingleImageContentGenerationJobResult(
			response.channel,
			new Date(response.scheduled_at),
			TextWithSingleImageContentData.fromResponse(response.data)
		);
	}
}

export class TextOnlyContentGenerationJobResult extends ContentGenerationJobResult {
	constructor(
		public readonly channel: ContentChannelName,
		public readonly scheduledAt: Date,
		public readonly data: TextOnlyContentData
	) {
		super(channel, scheduledAt);
	}
	static fromResponse(response: TextOnlyContentGenerationJobResultResponse) {
		return new TextOnlyContentGenerationJobResult(
			response.channel,
			new Date(response.scheduled_at),
			TextOnlyContentData.fromResponse(response.data)
		);
	}
}
