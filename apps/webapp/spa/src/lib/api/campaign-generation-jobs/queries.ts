import { createQuery } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { CampaignGenerationJobEndpoints } from './CampaignGenerationJobEndpoints';

export function useCampaignGenerationJob(
	brandIdGetter: () => string | undefined,
	jobIdGetter: () => string | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const jobId = jobIdGetter();
		return {
			queryKey: queryKeys.campaignGenerationJob(jobId ?? ''),
			queryFn: () => {
				if (!brandId) {
					throw new Error('Brand ID is required');
				}
				if (!jobId) {
					throw new Error('Job ID is required');
				}
				return CampaignGenerationJobEndpoints.get(brandId, jobId);
			},
			enabled: !!brandId && !!jobId,
			refetchInterval: (query) => {
				const job = query.state.data;
				if (!job) return false;
				if (job.status === 'pending' || job.status === 'in_progress') {
					return job.result?.content_brief ? 3000 : 1500;
				}
				return false;
			}
		};
	});
}

export { useAcceptCampaignGenerationJob, useCreateCampaignGenerationJob } from './mutations';
