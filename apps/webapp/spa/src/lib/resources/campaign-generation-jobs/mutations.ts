import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandCampaignCreationApi } from '$lib/api/generated/apis/BrandCampaignCreationApi';
import { BrandCampaignCreationContentPlanItemsApi } from '$lib/api/generated/apis/BrandCampaignCreationContentPlanItemsApi';
import type { CampaignCreationAcceptRequest } from '$lib/api/generated/models/CampaignCreationAcceptRequest';
import type { RestContentPlanItemUpdateRequest } from '$lib/api/generated/models/RestContentPlanItemUpdateRequest';
import { queryKeys } from '../queryKeys';

const creationApi = new BrandCampaignCreationApi(openApiConfiguration);
const contentPlanItemsApi = new BrandCampaignCreationContentPlanItemsApi(openApiConfiguration);

export function useCreateCampaignGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; requestData: string; files?: File[] }) => {
			const { brandId, requestData, files = [] } = parameters;
			const formData = new FormData();
			formData.append('request_data', requestData);
			for (const file of files) {
				formData.append('request_files', file);
			}
			return creationApi.brandCampaignCreationStart({ brandId, requestData }, async ({ init }) => ({
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
			queryClient.setQueryData(queryKeys.campaignGenerationJob(job.id), job);
		}
	}));
}

export function useAcceptCampaignGenerationJob() {
	return createMutation(() => ({
		mutationFn: (parameters: {
			brandId: string;
			jobId: string;
			request: CampaignCreationAcceptRequest;
		}) =>
			creationApi.brandCampaignCreationAccept({
				brandId: parameters.brandId,
				jobId: parameters.jobId,
				campaignCreationAcceptRequest: parameters.request
			})
	}));
}

export function useUpdateContentPlanItem() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: {
			brandId: string;
			jobId: string;
			contentPlanItemId: string;
			update: RestContentPlanItemUpdateRequest;
		}) =>
			contentPlanItemsApi.brandCampaignCreationContentPlanItemsUpdateContentPlanItem({
				brandId: parameters.brandId,
				jobId: parameters.jobId,
				contentPlanItemId: parameters.contentPlanItemId,
				restContentPlanItemUpdateRequest: parameters.update
			}),
		onSuccess: (_data, variables) => {
			queryClient.invalidateQueries({
				queryKey: queryKeys.campaignGenerationJob(variables.jobId)
			});
		}
	}));
}

export function useDeleteContentPlanItem() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; jobId: string; contentPlanItemId: string }) =>
			contentPlanItemsApi.brandCampaignCreationContentPlanItemsRemoveContentPlanItem(parameters),
		onSuccess: (_data, variables) => {
			queryClient.invalidateQueries({
				queryKey: queryKeys.campaignGenerationJob(variables.jobId)
			});
		}
	}));
}
