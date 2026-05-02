import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandGenerationApi } from '$lib/api/generated/apis/BrandGenerationApi';
import type { BrandGenerationJobCreateRequestBody } from '$lib/api/generated/models/BrandGenerationJobCreateRequestBody';
import type { BrandGenerationJobAcceptRequest } from '$lib/api/generated/models/BrandGenerationJobAcceptRequest';
import { queryKeys } from '../queryKeys';

const api = new BrandGenerationApi(openApiConfiguration);

export function useStartBrandGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (body: BrandGenerationJobCreateRequestBody) =>
			api.brandGenerationStart({ brandGenerationJobCreateRequestBody: body }),
		onSuccess: (job) => {
			queryClient.setQueryData(queryKeys.brandGenerationJob(job.id), job);
		}
	}));
}

export function useAcceptBrandGenerationJob() {
	return createMutation(() => ({
		mutationFn: (parameters: { jobId: string; body: BrandGenerationJobAcceptRequest }) =>
			api.brandGenerationAccept({
				jobId: parameters.jobId,
				brandGenerationJobAcceptRequest: parameters.body
			})
	}));
}
