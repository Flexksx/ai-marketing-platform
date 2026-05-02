import { createQuery } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandCampaignsApi } from '$lib/api/generated/apis/BrandCampaignsApi';
import type { CampaignState } from '$lib/api/generated/models/CampaignState';
import { queryKeys } from '../queryKeys';

const api = new BrandCampaignsApi(openApiConfiguration);

export function useCampaignsForBrand(
	brandIdGetter: () => string | undefined,
	paramsGetter?: () =>
		| { state?: CampaignState | null; limit?: number; offset?: number }
		| undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const params = paramsGetter?.() ?? { offset: 0, limit: 100, state: null };
		return {
			queryKey: queryKeys.campaignsForBrand(brandId ?? '', { brandId: brandId ?? '', ...params }),
			queryFn: () => api.brandCampaignsList({ brandId: brandId!, ...params }),
			enabled: !!brandId
		};
	});
}
