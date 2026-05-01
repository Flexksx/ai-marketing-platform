import axios from 'axios';
import type { BrandStatsResponse, BrandStatsListRequest } from './brand_stats.types';
import { createBackendClient } from '$lib/backend';

const get = async ({
	brandId,
	accessToken
}: {
	brandId: string;
	accessToken: string;
}): Promise<BrandStatsResponse> => {
	try {
		const client = createBackendClient(accessToken);
		const response = await client.get<BrandStatsResponse>(`/brand_stats/${brandId}`);
		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error)) {
			const errorMessage =
				error.response?.data?.detail ||
				error.response?.data?.error ||
				error.message ||
				'Unknown error';
			throw new Error(`Failed to get brand stats: ${errorMessage}`);
		}
		throw error;
	}
};

const list = async ({
	accessToken,
	props
}: {
	accessToken: string;
	props?: BrandStatsListRequest;
}): Promise<BrandStatsResponse[]> => {
	try {
		const client = createBackendClient(accessToken);
		const params = new URLSearchParams();
		if (props?.limit) params.append('limit', props.limit.toString());
		if (props?.offset) params.append('offset', props.offset.toString());

		const url = `/brand_stats${params.toString() ? `?${params.toString()}` : ''}`;
		const response = await client.get<BrandStatsResponse[]>(url);
		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error)) {
			const errorMessage =
				error.response?.data?.detail ||
				error.response?.data?.error ||
				error.message ||
				'Unknown error';
			throw new Error(`Failed to list brand stats: ${errorMessage}`);
		}
		throw error;
	}
};

export const BrandStatsService = {
	get,
	list
};

