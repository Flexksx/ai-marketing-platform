import { createQuery } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandContentApi } from '$lib/api/generated/apis/BrandContentApi';
import type { BrandContentSearchRequest } from '$lib/api/generated/apis/BrandContentApi';
import { queryKeys } from '../queryKeys';

const api = new BrandContentApi(openApiConfiguration);

export function useContentForBrand(
	brandIdGetter: () => string | undefined,
	paramsGetter?: () => Omit<BrandContentSearchRequest, 'brandId'> | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const params = paramsGetter?.() ?? { offset: 0, limit: 1000 };
		return {
			queryKey: queryKeys.contentForBrand(brandId ?? '', { brandId: brandId ?? '', ...params }),
			queryFn: () => api.brandContentSearch({ brandId: brandId!, ...params }),
			enabled: !!brandId
		};
	});
}
