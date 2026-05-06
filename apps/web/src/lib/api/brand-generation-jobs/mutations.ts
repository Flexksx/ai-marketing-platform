import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { BrandGenerationJobEndpoints } from './BrandGenerationJobEndpoints';
import type { BrandGenerationJobAcceptRequest } from './schema/BrandGenerationJobAcceptRequest';
import type { BrandGenerationJobCreateRequestBody } from './schema/BrandGenerationJobCreateRequestBody';

export function useStartBrandGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (body: BrandGenerationJobCreateRequestBody) =>
			BrandGenerationJobEndpoints.start(body),
		onSuccess: (job) => {
			queryClient.setQueryData(queryKeys.brandGenerationJob(job.id), job);
		}
	}));
}

export function useAcceptBrandGenerationJob() {
	return createMutation(() => ({
		mutationFn: ({ jobId, body }: { jobId: string; body: BrandGenerationJobAcceptRequest }) =>
			BrandGenerationJobEndpoints.accept(jobId, body)
	}));
}
