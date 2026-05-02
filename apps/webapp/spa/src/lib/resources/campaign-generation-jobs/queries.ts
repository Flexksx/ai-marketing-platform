import { createQuery } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandCampaignCreationApi } from '$lib/api/generated/apis/BrandCampaignCreationApi';
import { JobStatus } from '$lib/api/generated/models/JobStatus';
import { queryKeys } from '../queryKeys';

const api = new BrandCampaignCreationApi(openApiConfiguration);

export function useCampaignGenerationJob(
	brandIdGetter: () => string | undefined,
	jobIdGetter: () => string | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const jobId = jobIdGetter();
		return {
			queryKey: queryKeys.campaignGenerationJob(jobId ?? ''),
			queryFn: () => api.brandCampaignCreationGet({ brandId: brandId!, jobId: jobId! }),
			enabled: !!brandId && !!jobId,
			refetchInterval: (query) => {
				const job = query.state.data;
				if (!job) return false;
				if (job.status === JobStatus.pending || job.status === JobStatus.inProgress) {
					return job.result?.contentBrief ? 3000 : 1500;
				}
				return false;
			}
		};
	});
}
