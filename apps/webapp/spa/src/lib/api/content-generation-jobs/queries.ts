import { createQuery } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { ContentGenerationJobEndpoints } from './ContentGenerationJobEndpoints';
import { JobStatus } from '../job/JobStatus';

export function useContentGenerationJob(
	brandIdGetter: () => string | undefined,
	jobIdGetter: () => string | undefined
) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		const jobId = jobIdGetter();
		return {
			queryKey: queryKeys.contentGenerationJob(jobId ?? ''),
			queryFn: () => {
				if (!brandId) {
					throw new Error('Brand ID is required');
				}
				if (!jobId) {
					throw new Error('Job ID is required');
				}
				return ContentGenerationJobEndpoints.get(brandId, jobId);
			},
			enabled: !!brandId && !!jobId,
			refetchInterval: (query) => {
				const job = query.state.data;
				if (!job) return false;
				if (job.status === JobStatus.PENDING || job.status === JobStatus.IN_PROGRESS) {
					return 5000;
				}
				return false;
			}
		};
	});
}

export function useContentGenerationJobs(brandIdGetter: () => string | undefined) {
	return createQuery(() => {
		const brandId = brandIdGetter();
		return {
			queryKey: queryKeys.contentGenerationJobs(brandId ?? ''),
			queryFn: () => {
				if (!brandId) {
					throw new Error('Brand ID is required');
				}
				return ContentGenerationJobEndpoints.search(brandId);
			},
			enabled: !!brandId
		};
	});
}
