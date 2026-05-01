import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { BrandEndpoints } from './BrandEndpoints';
import type { BrandCreateRequest } from './schema/BrandCreateRequest';
import type { BrandUpdateRequest } from './schema/BrandUpdateRequest';

export function useCreateBrand() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (brand: BrandCreateRequest) => BrandEndpoints.create(brand),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		}
	}));
}

export function useUpdateBrand() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: async (parameters: { brandId?: string; request: BrandUpdateRequest }) => {
			if (!parameters.brandId) {
				throw new Error('Brand ID is required');
			}
			await BrandEndpoints.update(parameters.brandId, parameters.request);
			return parameters.brandId;
		},
		onSuccess: (_, variables) => {
			queryClient.invalidateQueries({ queryKey: queryKeys.brand(variables.brandId ?? '') });
			queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		}
	}));
}

export function useDeleteBrand() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: async (brandId?: string) => {
			if (!brandId) {
				throw new Error('Brand ID is required');
			}
			await BrandEndpoints.remove(brandId);
			return brandId;
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		}
	}));
}
