import axios from 'axios';
import type { BrandStatsResponse, BrandStatsListRequest } from './brand_stats.types';
import { createBackendClient } from '$lib/backend/client';

export type BrandStatsGetResponse = BrandStatsResponse;

export type BrandStatsListResponse = BrandStatsResponse[];

const getBrandStatsApiUrl = () => '/api/brand_stats';

export class BrandStatsEndpoints {
	static async get(accessToken: string, brandId: string): Promise<BrandStatsGetResponse> {
		const client = createBackendClient(accessToken);
		try {
			const response = await client.get<BrandStatsGetResponse>(
				`${getBrandStatsApiUrl()}/${brandId}`
			);
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
	}

	static async list(accessToken: string, props?: BrandStatsListRequest): Promise<BrandStatsListResponse> {
		const client = createBackendClient(accessToken);
		const params = new URLSearchParams();
		if (props?.limit !== undefined) params.append('limit', props.limit.toString());
		if (props?.offset !== undefined) params.append('offset', props.offset.toString());

		const url = `${getBrandStatsApiUrl()}${params.toString() ? `?${params.toString()}` : ''}`;

		try {
			const response = await client.get<BrandStatsListResponse>(url);
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
	}
}
