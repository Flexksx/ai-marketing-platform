import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { ContentGenerationJobEndpoints } from './ContentGenerationJobEndpoints';
import type { ContentGenerationJobCreateRequest } from './ContentGenerationJobCreateRequest';

export function useCreateContentGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { request: ContentGenerationJobCreateRequest; file?: File }) => {
			const { request, file } = parameters;
			return ContentGenerationJobEndpoints.create(request.brand_id, request, file);
		},
		onSuccess: (job) => {
			queryClient.setQueryData(queryKeys.contentGenerationJob(job.id), job);
			queryClient.invalidateQueries({
				queryKey: queryKeys.contentGenerationJobs(job.brandId)
			});
		}
	}));
}

export function useAcceptContentGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; jobId: string }) =>
			ContentGenerationJobEndpoints.accept(parameters.brandId, parameters.jobId),
		onSuccess: (_content, variables) => {
			queryClient.invalidateQueries({
				queryKey: ['content', 'brand', variables.brandId]
			});
		}
	}));
}
