import { ContentFormat } from './ContentFormat';

export interface TextOnlyContentDataResponse {
	content_format: ContentFormat.TEXT;
	caption: string;
}

export interface TextWithSingleImageContentDataResponse {
	content_format: ContentFormat.TEXT_WITH_SINGLE_IMAGE;
	caption: string;
	image_url: string;
}

export type ContentDataResponse =
	| TextOnlyContentDataResponse
	| TextWithSingleImageContentDataResponse;

export abstract class ContentData {
	public abstract readonly contentFormat: ContentFormat;
	constructor() {}

	static fromResponse(response: ContentDataResponse): ContentData {
		switch (response.content_format) {
			case ContentFormat.TEXT_WITH_SINGLE_IMAGE:
				return TextWithSingleImageContentData.fromResponse(response);
			case ContentFormat.TEXT:
				return TextOnlyContentData.fromResponse(response);

			default:
				throw new Error(`Unknown content format`);
		}
	}
}

export class TextWithSingleImageContentData extends ContentData {
	public readonly contentFormat = ContentFormat.TEXT_WITH_SINGLE_IMAGE;
	constructor(
		public readonly caption: string,
		public readonly imageUrl: string
	) {
		super();
	}
	static fromResponse(
		response: TextWithSingleImageContentDataResponse
	): TextWithSingleImageContentData {
		return new TextWithSingleImageContentData(response.caption, response.image_url);
	}
}

export class TextOnlyContentData extends ContentData {
	public readonly contentFormat = ContentFormat.TEXT;
	constructor(public readonly caption: string) {
		super();
	}

	static fromResponse(response: TextOnlyContentDataResponse): TextOnlyContentData {
		return new TextOnlyContentData(response.caption);
	}
}
