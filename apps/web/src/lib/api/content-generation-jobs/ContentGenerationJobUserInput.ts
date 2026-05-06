import type { ContentChannelName } from '../content-channel/ContentChannelName';
import { ContentGenerationJobWorkflowType } from './ContentGenerationJobWorkflowType';

export interface BaseContentGenerationJobUserInputResponse {
	prompt: string;
	channel: ContentChannelName;
	scheduled_at: string;
}

export interface FromUserMediaTextWithSingleImageContentGenerationJobUserInputResponse
	extends BaseContentGenerationJobUserInputResponse {
	workflow_type: ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA;
	image_url: string;
}

export interface AIGeneratedTextWithSingleImageContentGenerationJobUserInputResponse
	extends BaseContentGenerationJobUserInputResponse {
	workflow_type: ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED;
}

export interface ProductLifestyleTextWithSingleImageContentGenerationJobUserInputResponse
	extends BaseContentGenerationJobUserInputResponse {
	workflow_type: ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE;
}

export type ContentGenerationJobUserInputResponse =
	| FromUserMediaTextWithSingleImageContentGenerationJobUserInputResponse
	| AIGeneratedTextWithSingleImageContentGenerationJobUserInputResponse
	| ProductLifestyleTextWithSingleImageContentGenerationJobUserInputResponse;

export abstract class ContentGenerationJobUserInput {
	public abstract readonly workflowType: ContentGenerationJobWorkflowType;
	constructor(
		public prompt: string,
		public channel: ContentChannelName,
		public scheduledAt: Date
	) {}

	static fromResponse(response: ContentGenerationJobUserInputResponse) {
		switch (response.workflow_type) {
			case ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA:
				return FromUserMediaContentGenerationJobUserInput.fromResponse(response);
			case ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED:
				return AIGeneratedTextWithSingleImageContentGenerationJobUserInput.fromResponse(response);
			case ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE:
				return ProductLifestyleTextWithSingleImageContentGenerationJobUserInput.fromResponse(
					response
				);
			default:
				throw new Error(`Unknown workflow type: ${response}`);
		}
	}
}

export class FromUserMediaContentGenerationJobUserInput extends ContentGenerationJobUserInput {
	public readonly workflowType =
		ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA;
	constructor(
		public prompt: string,
		public channel: ContentChannelName,
		public scheduledAt: Date,
		public imageUrl: string
	) {
		super(prompt, channel, scheduledAt);
	}
	static fromResponse(
		response: FromUserMediaTextWithSingleImageContentGenerationJobUserInputResponse
	) {
		return new FromUserMediaContentGenerationJobUserInput(
			response.prompt,
			response.channel,
			new Date(response.scheduled_at),
			response.image_url
		);
	}
}

export class AIGeneratedTextWithSingleImageContentGenerationJobUserInput extends ContentGenerationJobUserInput {
	public readonly workflowType =
		ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED;
	constructor(
		public prompt: string,
		public channel: ContentChannelName,
		public scheduledAt: Date
	) {
		super(prompt, channel, scheduledAt);
	}
	static fromResponse(
		response: AIGeneratedTextWithSingleImageContentGenerationJobUserInputResponse
	) {
		return new AIGeneratedTextWithSingleImageContentGenerationJobUserInput(
			response.prompt,
			response.channel,
			new Date(response.scheduled_at)
		);
	}
}

export class ProductLifestyleTextWithSingleImageContentGenerationJobUserInput extends ContentGenerationJobUserInput {
	public readonly workflowType =
		ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE;
	constructor(
		public readonly prompt: string,
		public readonly channel: ContentChannelName,
		public readonly scheduledAt: Date
	) {
		super(prompt, channel, scheduledAt);
	}
	static fromResponse(
		response: ProductLifestyleTextWithSingleImageContentGenerationJobUserInputResponse
	) {
		return new ProductLifestyleTextWithSingleImageContentGenerationJobUserInput(
			response.prompt,
			response.channel,
			new Date(response.scheduled_at)
		);
	}
}
