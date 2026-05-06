import axios from 'axios';
import type { AxiosInstance } from 'axios';

const getBackendUrl = (): string => {
	const backendUrl =
		typeof window !== 'undefined'
			? import.meta.env.PUBLIC_BACKEND_URL || 'http://localhost:8000'
			: process.env.BACKEND_URL || process.env.PUBLIC_BACKEND_URL || 'http://localhost:8000';
	return backendUrl.replace(/\/$/, '');
};

export const createBackendClient = (accessToken?: string): AxiosInstance => {
	const backendUrl = getBackendUrl();
	const headers: Record<string, string> = {
		'Content-Type': 'application/json'
	};

	if (accessToken) {
		headers.Authorization = `Bearer ${accessToken}`;
	}

	return axios.create({
		baseURL: backendUrl,
		headers
	});
};

export const backendClient = createBackendClient();
