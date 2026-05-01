import { queryKeys } from '../shared/queryKeys';
import { CampaignEndpoints } from './CampaignEndpoints';
import { createQuery } from '@tanstack/svelte-query';
import type { CampaignListRequest } from './CampaignListRequest';

export function useCampaignsForBrand(
	brandIdGetter: () => string | undefined,
	paramsGetter?: () => CampaignListRequest | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const params = paramsGetter?.() ?? { offset: 0, limit: 100, state: null };
		return {
			queryKey: queryKeys.campaignsForBrand(brandId ?? '', params),
			queryFn: async () => {
				if (!brandId) {
					throw new Error('Brand ID is required');
				}
				return CampaignEndpoints.listForBrand(brandId, params);
			},
			enabled: !!brandId
		};
	});
}
