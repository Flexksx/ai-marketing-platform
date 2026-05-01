import { Campaign, type CampaignResponse } from '$lib/api/campaign/Campaign';
import type { ContentDataResponse } from '$lib/api/content/ContentData';
import axios from 'axios';
import { CampaignGenerationJob, type CampaignGenerationJobResponse } from './CampaignGenerationJob';
import {
	CampaignContentPlanItem,
	type CampaignContentPlanItemResponse
} from './CampaignGenerationJobResult';
import type { CampaignGenerationJobAcceptRequest } from './campaign-generation-job.schema';
import type { CampaignGenerationJobCreateRequest } from './CampaignGenerationJobCreateRequest';

const BASE_URL = '/api/brands';

const getUrl = (brandId: string, jobId?: string, action?: string) => {
	if (!jobId) return `${BASE_URL}/${brandId}/campaigns/create`;
	if (action) return `${BASE_URL}/${brandId}/campaigns/create/${jobId}/${action}`;
	return `${BASE_URL}/${brandId}/campaigns/create/${jobId}`;
};

const getContentPlanItemUrl = (brandId: string, jobId: string, itemId: string) =>
	`${BASE_URL}/${brandId}/campaigns/create/${jobId}/content_plan_items/${itemId}`;

export interface ContentPlanItemUpdateRequest {
	scheduled_at?: string | null;
	content_data?: ContentDataResponse | null;
}

const create = async (
	brandId: string,
	data: CampaignGenerationJobCreateRequest,
	files: File[] = []
): Promise<CampaignGenerationJob> => {
	const formData = new FormData();

	const workflowType = data.workflow_type || 'AI_GENERATED';
	const userInput: Record<string, string | string[] | undefined> = {
		workflow_type: workflowType,
		prompt: data.prompt,
		start_date: data.start_date,
		end_date: data.end_date,
		channels: data.channels
	};

	if (workflowType === 'USER_MEDIA_ONLY' || workflowType === 'PRODUCT_LIFESTYLE') {
		userInput.image_urls = [];
	}

	const requestPayload = {
		brand_id: brandId,
		workflow_type: workflowType,
		user_input: userInput
	};

	formData.append('request_data', JSON.stringify(requestPayload));

	for (const file of files) {
		formData.append('request_files', file);
	}

	const response = await axios.post<CampaignGenerationJobResponse>(getUrl(brandId), formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	return CampaignGenerationJob.fromResponse(response.data);
};

const get = async (brandId: string, jobId: string): Promise<CampaignGenerationJob> => {
	try {
		const response = await axios.get<CampaignGenerationJobResponse>(getUrl(brandId, jobId));
		return CampaignGenerationJob.fromResponse(response.data);
	} catch (error) {
		if (axios.isAxiosError(error) && error.response?.status === 404) {
			throw new Error(`Campaign generation job ${jobId} not found`);
		}
		throw error;
	}
};

const accept = async (
	brandId: string,
	jobId: string,
	data: CampaignGenerationJobAcceptRequest
): Promise<Campaign> => {
	const response = await axios.post<CampaignResponse>(getUrl(brandId, jobId, 'accept'), data);
	return Campaign.fromResponse(response.data);
};

const updateContentPlanItem = async (
	brandId: string,
	jobId: string,
	itemId: string,
	payload: ContentPlanItemUpdateRequest
): Promise<CampaignContentPlanItem> => {
	const response = await axios.put<CampaignContentPlanItemResponse>(
		getContentPlanItemUrl(brandId, jobId, itemId),
		payload
	);

	return CampaignContentPlanItem.fromResponse(response.data);
};

const deleteContentPlanItem = async (
	brandId: string,
	jobId: string,
	itemId: string
): Promise<void> => {
	await axios.delete(getContentPlanItemUrl(brandId, jobId, itemId));
};

export const CampaignGenerationJobEndpoints = {
	create,
	get,
	accept,
	updateContentPlanItem,
	deleteContentPlanItem
};
