import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandContentGenerationJobsApi } from '$lib/api/generated/apis/BrandContentGenerationJobsApi';
import { queryKeys } from '../queryKeys';

const api = new BrandContentGenerationJobsApi(openApiConfiguration);

export function useCreateContentGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; requestData: string; file?: File }) => {
			const { brandId, requestData, file } = parameters;
			const formData = new FormData();
			formData.append('request_data', requestData);
			if (file) {
				formData.append('request_file', file);
			}
			return api.brandContentGenerationJobsStart({ brandId, requestData }, async ({ init }) => ({
				...init,
				body: formData,
				headers: Object.fromEntries(
					Object.entries(init.headers as Record<string, string>).filter(
						([key]) => key.toLowerCase() !== 'content-type'
					)
				)
			}));
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
			api.brandContentGenerationJobsAccept(parameters),
		onSuccess: (_content, variables) => {
			queryClient.invalidateQueries({
				queryKey: queryKeys.contentForBrand(variables.brandId)
			});
		}
	}));
}
