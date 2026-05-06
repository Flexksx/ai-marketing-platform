import type { ContentChannelName } from '../content-channel/ContentChannelName';
import { CampaignGenerationJobWorkflowType } from './CampaignGenerationJobWorkflowType';

export interface BaseUserInputResponse {
	prompt: string;
	start_date: string;
	end_date: string;
	channels: ContentChannelName[];
}

export interface UserMediaOnlyInputResponse extends BaseUserInputResponse {
	workflow_type: CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY;
	image_urls: string[];
}

export interface AiGeneratedInputResponse extends BaseUserInputResponse {
	workflow_type: CampaignGenerationJobWorkflowType.AI_GENERATED;
}

export interface ProductLifestyleInputResponse extends BaseUserInputResponse {
	workflow_type: CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE;
	image_urls: string[];
}

export type CampaignGenerationJobUserInputResponse =
	| UserMediaOnlyInputResponse
	| AiGeneratedInputResponse
	| ProductLifestyleInputResponse;

export abstract class CampaignGenerationJobUserInput {
	public abstract readonly workflowType: CampaignGenerationJobWorkflowType;
	constructor(
		public readonly prompt: string,
		public readonly startDate: Date,
		public readonly endDate: Date,
		public readonly channels: ContentChannelName[]
	) {}
	static fromResponse(
		response: CampaignGenerationJobUserInputResponse
	): CampaignGenerationJobUserInput {
		switch (response.workflow_type) {
			case CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY:
				return UserMediaOnlyCampaignGenerationJobUserInput.fromResponse(response);
			case CampaignGenerationJobWorkflowType.AI_GENERATED:
				return AiGeneratedCampaignGenerationJobUserInput.fromResponse(response);
			case CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE:
				return ProductLifestyleCampaignGenerationJobUserInput.fromResponse(response);
			default:
				throw new Error(`Unhandled workflow type`);
		}
	}
}

export class UserMediaOnlyCampaignGenerationJobUserInput extends CampaignGenerationJobUserInput {
	public readonly workflowType = CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY;
	public readonly imageUrls: string[];
	constructor(
		prompt: string,
		startDate: Date,
		endDate: Date,
		channels: ContentChannelName[],
		imageUrls: string[]
	) {
		super(prompt, startDate, endDate, channels);
		this.imageUrls = imageUrls;
	}
	static fromResponse(
		response: UserMediaOnlyInputResponse
	): UserMediaOnlyCampaignGenerationJobUserInput {
		return new UserMediaOnlyCampaignGenerationJobUserInput(
			response.prompt,
			new Date(response.start_date),
			new Date(response.end_date),
			response.channels,
			response.image_urls
		);
	}
}

export class AiGeneratedCampaignGenerationJobUserInput extends CampaignGenerationJobUserInput {
	public readonly workflowType = CampaignGenerationJobWorkflowType.AI_GENERATED;
	constructor(prompt: string, startDate: Date, endDate: Date, channels: ContentChannelName[]) {
		super(prompt, startDate, endDate, channels);
	}
	static fromResponse(
		response: AiGeneratedInputResponse
	): AiGeneratedCampaignGenerationJobUserInput {
		return new AiGeneratedCampaignGenerationJobUserInput(
			response.prompt,
			new Date(response.start_date),
			new Date(response.end_date),
			response.channels
		);
	}
}

export class ProductLifestyleCampaignGenerationJobUserInput extends CampaignGenerationJobUserInput {
	public readonly workflowType = CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE;
	public readonly imageUrls: string[];
	constructor(
		prompt: string,
		startDate: Date,
		endDate: Date,
		channels: ContentChannelName[],
		imageUrls: string[]
	) {
		super(prompt, startDate, endDate, channels);
		this.imageUrls = imageUrls;
	}
	static fromResponse(
		response: ProductLifestyleInputResponse
	): ProductLifestyleCampaignGenerationJobUserInput {
		return new ProductLifestyleCampaignGenerationJobUserInput(
			response.prompt,
			new Date(response.start_date),
			new Date(response.end_date),
			response.channels,
			response.image_urls
		);
	}
}
