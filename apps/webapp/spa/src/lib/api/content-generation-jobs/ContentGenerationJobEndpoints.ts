import { Content, type ContentResponse } from '$lib/api/content/Content';
import axios from 'axios';
import { ContentGenerationJob, type ContentGenerationJobResponse } from './ContentGenerationJob';
import type { ContentGenerationJobCreateRequest } from './ContentGenerationJobCreateRequest';

const BASE_URL = '/api/brands';

const getUrl = (brandId: string, jobId?: string, action?: string) => {
	if (!jobId) return `${BASE_URL}/${brandId}/content-generation`;
	if (action) return `${BASE_URL}/${brandId}/content-generation/${jobId}/${action}`;
	return `${BASE_URL}/${brandId}/content-generation/${jobId}`;
};

const create = async (
	brandId: string,
	data: ContentGenerationJobCreateRequest,
	file?: File
): Promise<ContentGenerationJob> => {
	const formData = new FormData();

	const requestPayload: ContentGenerationJobCreateRequest = {
		brand_id: brandId,
		user_input: data.user_input,
		content_format: data.content_format
	};

	formData.append('request_data', JSON.stringify(requestPayload));

	if (file) {
		formData.append('request_file', file);
	}

	const response = await axios.post<ContentGenerationJobResponse>(getUrl(brandId), formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
	return ContentGenerationJob.fromResponse(response.data);
};

const get = async (brandId: string, jobId: string): Promise<ContentGenerationJob> => {
	try {
		const response = await axios.get<ContentGenerationJobResponse>(getUrl(brandId, jobId));
		return ContentGenerationJob.fromResponse(response.data);
	} catch (error) {
		if (axios.isAxiosError(error) && error.response?.status === 404) {
			throw new Error(`Content generation job ${jobId} not found`);
		}
		throw error;
	}
};

const search = async (brandId: string): Promise<ContentGenerationJob[]> => {
	const response = await axios.get<ContentGenerationJobResponse[]>(
		`${BASE_URL}/${brandId}/content-generation`,
		{
			params: { brand_id: brandId }
		}
	);
	return response.data.map(ContentGenerationJob.fromResponse);
};

const accept = async (brandId: string, jobId: string): Promise<Content> => {
	const response = await axios.post<ContentResponse>(getUrl(brandId, jobId, 'accept'));
	return Content.fromResponse(response.data);
};

export const ContentGenerationJobEndpoints = {
	create,
	get,
	search,
	accept
};
