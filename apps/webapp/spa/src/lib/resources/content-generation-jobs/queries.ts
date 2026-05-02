import { createQuery } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandContentGenerationJobsApi } from '$lib/api/generated/apis/BrandContentGenerationJobsApi';
import { JobStatus } from '$lib/api/generated/models/JobStatus';
import { queryKeys } from '../queryKeys';

const api = new BrandContentGenerationJobsApi(openApiConfiguration);

export function useContentGenerationJob(
	brandIdGetter: () => string | undefined,
	jobIdGetter: () => string | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const jobId = jobIdGetter();
		return {
			queryKey: queryKeys.contentGenerationJob(jobId ?? ''),
			queryFn: () =>
				api.brandContentGenerationJobsGet({ brandId: brandId!, jobId: jobId! }),
			enabled: !!brandId && !!jobId,
			refetchInterval: (query) => {
				const job = query.state.data;
				if (!job) return false;
				if (job.status === JobStatus.pending || job.status === JobStatus.inProgress) {
					return 5000;
				}
				return false;
			}
		};
	});
}
