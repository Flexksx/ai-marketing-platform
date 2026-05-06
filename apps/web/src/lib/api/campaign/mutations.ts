import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { CampaignEndpoints } from './CampaignEndpoints';

export function useDeleteCampaign() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; campaignId: string }) =>
			CampaignEndpoints.remove(parameters.brandId, parameters.campaignId),
		onSuccess: (_, variables) => {
			queryClient.invalidateQueries({
				queryKey: ['campaigns', 'brand', variables.brandId]
			});
		}
	}));
}
