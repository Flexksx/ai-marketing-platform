import { createQuery } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandsApi } from '$lib/api/generated/apis/BrandsApi';
import { queryKeys } from '../queryKeys';

const api = new BrandsApi(openApiConfiguration);

export function useBrand(idGetter: () => string | undefined) {
	return createQuery(() => {
		const id = idGetter();
		return {
			queryKey: queryKeys.brand(id ?? ''),
			queryFn: () => api.brandsGet({ brandId: id! }),
			enabled: !!id
		};
	});
}

export function useBrands(
	paramsGetter?: () => { name?: string; limit?: number; offset?: number } | undefined
) {
	return createQuery(() => {
		const params = paramsGetter?.() ?? { offset: 0, limit: 100 };
		return {
			queryKey: queryKeys.brands(params),
			queryFn: () => api.brandsSearch(params)
		};
	});
}
