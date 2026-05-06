import { createMutation, useQueryClient } from '@tanstack/svelte-query';
import { queryKeys } from '../shared/queryKeys';
import { CampaignGenerationJobEndpoints } from './CampaignGenerationJobEndpoints';
import type {
	CampaignGenerationJobAcceptRequest,
	PostingPlanItemModification
} from './campaign-generation-job.schema';
import type { CampaignGenerationJobCreateRequest } from './CampaignGenerationJobCreateRequest';
import type { CampaignGenerationJob } from './CampaignGenerationJob';

export function useCreateCampaignGenerationJob() {
	const queryClient = useQueryClient();
	return createMutation(() => ({
		mutationFn: (parameters: { request: CampaignGenerationJobCreateRequest; files?: File[] }) => {
			const { request, files = [] } = parameters;
			return CampaignGenerationJobEndpoints.create(request.brand_id, request, files);
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
			request: CampaignGenerationJobAcceptRequest;
		}) =>
			CampaignGenerationJobEndpoints.accept(
				parameters.brandId,
				parameters.jobId,
				parameters.request
			)
	}));
}

export function useUpdateContentPlanItem() {
	const queryClient = useQueryClient();

	return createMutation(() => ({
		mutationFn: (parameters: {
			brandId: string;
			jobId: string;
			itemId: string;
			modification: PostingPlanItemModification;
		}) => {
			const { brandId, jobId, itemId, modification } = parameters;

			const payload = {
				scheduled_at: modification.scheduled_at ?? undefined,
				content_data:
					modification.caption || modification.image_url
						? {
								content_format: modification.image_url ? 'TEXT_WITH_SINGLE_IMAGE' : 'TEXT',
								caption: modification.caption ?? '',
								image_url: modification.image_url ?? undefined
							}
						: undefined
			};

			return CampaignGenerationJobEndpoints.updateContentPlanItem(brandId, jobId, itemId, payload);
		},
		onSuccess: (_data, parameters) => {
			queryClient.invalidateQueries({
				queryKey: queryKeys.campaignGenerationJob(parameters.jobId)
			});
		}
	}));
}

export function useDeleteContentPlanItem() {
	const queryClient = useQueryClient();

	return createMutation(() => ({
		mutationFn: (parameters: { brandId: string; jobId: string; itemId: string }) =>
			CampaignGenerationJobEndpoints.deleteContentPlanItem(
				parameters.brandId,
				parameters.jobId,
				parameters.itemId
			),
		onSuccess: (_data, variables) => {
			queryClient.invalidateQueries({
				queryKey: queryKeys.campaignGenerationJob(variables.jobId)
			});
		}
	}));
}
