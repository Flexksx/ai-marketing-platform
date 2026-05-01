import { Brand } from '$lib/api/brands/model/Brand';
import type { BrandResponse } from '$lib/api/brands/schema/BrandResponse';
import axios from 'axios';
import { BrandGenerationJob } from './model/BrandGenerationJob';
import type { BrandGenerationJobAcceptRequest } from './schema/BrandGenerationJobAcceptRequest';
import type { BrandGenerationJobCreateRequestBody } from './schema/BrandGenerationJobCreateRequestBody';
import type { BrandGenerationJobResponse } from './schema/BrandGenerationJobResponse';

const BASE_URL = '/api/brand-generation';

const getUrl = (jobId?: string, action?: string) => {
	if (!jobId) return BASE_URL;
	if (action) return `${BASE_URL}/${jobId}/${action}`;
	return `${BASE_URL}/${jobId}`;
};

const start = async (body: BrandGenerationJobCreateRequestBody): Promise<BrandGenerationJob> => {
	const response = await axios.post<BrandGenerationJobResponse>(getUrl(), body);
	return BrandGenerationJob.fromResponse(response.data);
};

const get = async (jobId: string): Promise<BrandGenerationJob> => {
	try {
		const response = await axios.get<BrandGenerationJobResponse>(getUrl(jobId));
		return BrandGenerationJob.fromResponse(response.data);
	} catch (error) {
		if (axios.isAxiosError(error) && error.response?.status === 404) {
			throw new Error(`Brand generation job ${jobId} not found`);
		}
		throw error;
	}
};

const accept = async (jobId: string, body: BrandGenerationJobAcceptRequest): Promise<Brand> => {
	const response = await axios.post<BrandResponse>(getUrl(jobId, 'accept'), body);
	return Brand.fromResponse(response.data);
};

export const BrandGenerationJobEndpoints = {
	start,
	get,
	accept
};
