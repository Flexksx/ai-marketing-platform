import { createQuery } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { ContentEndpoints } from './ContentEndpoints';
import type { ContentListRequest } from './ContentListRequest';

export function useContentForBrand(
	brandIdGetter: () => string | undefined,
	paramsGetter?: () => ContentListRequest | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const params = paramsGetter?.() ?? { offset: 0, limit: 1000 };
		return {
			queryKey: queryKeys.contentForBrand(brandId ?? '', params),
			queryFn: () => {
				if (!brandId) {
					throw new Error('Brand ID is required');
				}
				return ContentEndpoints.list(brandId, params);
			},
			enabled: !!brandId
		};
	});
}
