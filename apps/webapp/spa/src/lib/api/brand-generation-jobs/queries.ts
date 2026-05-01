import { createQuery } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { BrandGenerationJobEndpoints } from './BrandGenerationJobEndpoints';

export function useBrandGenerationJob(jobIdGetter: () => string | undefined) {
	return createQuery(() => {
		const jobId = jobIdGetter();
		return {
			queryKey: queryKeys.brandGenerationJob(jobId ?? ''),
			queryFn: () => {
				if (!jobId) {
					throw new Error('Job ID is required');
				}
				return BrandGenerationJobEndpoints.get(jobId);
			},
			enabled: !!jobId,
			refetchInterval: (query) => {
				const job = query.state.data;
				if (!job) return false;
				if (job.status === 'pending' || job.status === 'in_progress') {
					return 2000;
				}
				return false;
			}
		};
	});
}
