import axios, { type AxiosRequestConfig } from 'axios';

function platformApiBaseUrl(): string {
	const fromEnv = import.meta.env.VITE_PLATFORM_API_URL;
	if (fromEnv != null && fromEnv !== "") {
		return fromEnv;
	}
	if (import.meta.env.DEV) {
		return "";
	}
	return "http://localhost:8080";
}

const PLATFORM_API_BASE_URL = platformApiBaseUrl();

export const platformApiInstance = axios.create({
  baseURL: PLATFORM_API_BASE_URL,
});

platformApiInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const customInstance = <T>(config: AxiosRequestConfig): Promise<T> => {
  return platformApiInstance(config).then(({ data }) => data);
};

export default customInstance;
