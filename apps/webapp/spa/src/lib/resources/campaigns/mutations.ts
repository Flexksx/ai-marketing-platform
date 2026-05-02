import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandCampaignsApi } from '$lib/api/generated/apis/BrandCampaignsApi';
import { queryKeys } from '../queryKeys';

const api = new BrandCampaignsApi(openApiConfiguration);

export function useDeleteCampaign() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; campaignId: string }) =>
			api.brandCampaignsDeleteCampaign(parameters),
		onSuccess: (_, variables) => {
			queryClient.invalidateQueries({
				queryKey: queryKeys.campaignsForBrand(variables.brandId)
			});
		}
	}));
}
