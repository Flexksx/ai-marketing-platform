import { queryKeys } from '../shared/queryKeys';
import { BrandEndpoints } from './BrandEndpoints';
import { createQuery } from '@tanstack/svelte-query';
import type { BrandListRequest } from './schema/BrandListRequest';

export function useBrand(idGetter: () => string | undefined) {
	return createQuery(() => {
		const id = idGetter();
		return {
			queryKey: queryKeys.brand(id ?? ''),
			queryFn: () => {
				if (!id) {
					throw new Error('Brand ID is required');
				}
				return BrandEndpoints.get(id);
			},
			enabled: !!id
		};
	});
}

export function useBrands(paramsGetter?: () => BrandListRequest | undefined) {
	return createQuery(() => {
		const params = paramsGetter?.() ?? { offset: 0, limit: 100, name: null };
		return {
			queryKey: queryKeys.brands(params),
			queryFn: () => BrandEndpoints.list(params)
		};
	});
}
