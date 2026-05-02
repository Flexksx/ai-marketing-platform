import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandsApi } from '$lib/api/generated/apis/BrandsApi';
import type { BrandCreateRequest } from '$lib/api/generated/models/BrandCreateRequest';
import type { BrandData } from '$lib/api/generated/models/BrandData';
import { queryKeys } from '../queryKeys';

const api = new BrandsApi(openApiConfiguration);

export function useCreateBrand() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (brand: BrandCreateRequest) => api.brandsCreate({ brandCreateRequest: brand }),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		}
	}));
}

export function useUpdateBrand() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: {
			brandId: string;
			name?: string;
			data: BrandData;
			logoFile?: File;
		}) => {
			const { brandId, name, data, logoFile } = parameters;
			const requestData = JSON.stringify({ name, data });
			const formData = new FormData();
			formData.append('request_data', requestData);
			if (logoFile) {
				formData.append('logo_file', logoFile);
			}
			return api.brandsUpdate(
				{ brandId, requestData },
				async ({ init }) => ({
					...init,
					body: formData,
					headers: Object.fromEntries(
						Object.entries(init.headers as Record<string, string>).filter(
							([key]) => key.toLowerCase() !== 'content-type'
						)
					)
				})
			);
		},
		onSuccess: (_result, variables) => {
			queryClient.invalidateQueries({ queryKey: queryKeys.brand(variables.brandId) });
			queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		}
	}));
}

export function useDeleteBrand() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (brandId: string) => api.brandsDelete({ brandId }),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		}
	}));
}
