import { createQuery } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandGenerationApi } from '$lib/api/generated/apis/BrandGenerationApi';
import { JobStatus } from '$lib/api/generated/models/JobStatus';
import { queryKeys } from '../queryKeys';

const api = new BrandGenerationApi(openApiConfiguration);

export function useBrandGenerationJob(jobIdGetter: () => string | undefined) {
	return createQuery(() => {
		const jobId = jobIdGetter();
		return {
			queryKey: queryKeys.brandGenerationJob(jobId ?? ''),
			queryFn: () => api.brandGenerationGet({ jobId: jobId! }),
			enabled: !!jobId,
			refetchInterval: (query) => {
				const job = query.state.data;
				if (!job) return false;
				if (job.status === JobStatus.pending || job.status === JobStatus.inProgress) {
					return 2000;
				}
				return false;
			}
		};
	});
}
