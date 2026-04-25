import axios, { type AxiosRequestConfig } from 'axios';

const PLATFORM_API_BASE_URL = import.meta.env?.VITE_PLATFORM_API_URL ?? 'http://localhost:8080';

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

export default <T>(config: AxiosRequestConfig): Promise<T> => {
  return platformApiInstance(config).then(({ data }) => data);
};
