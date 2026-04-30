import {
	type BrandResponse,
	type CreateBrandRequest,
	type UpdateBrandRequest,
	getBrands,
} from "@ai-marketing-platform/platform-api-client";
import { useMutation, useQueryClient } from "@tanstack/vue-query";

import { queryKeys } from "@/lib/queryKeys";

const brands = getBrands();

export const useCreateBrandMutation = () => {
	const queryClient = useQueryClient();
	return useMutation<BrandResponse, Error, CreateBrandRequest>({
		mutationFn: (body) => brands.create(body),
		onSuccess: () => {
			void queryClient.invalidateQueries({
				queryKey: queryKeys.brands(),
			});
		},
	});
};

export const useUpdateBrandMutation = () => {
	const queryClient = useQueryClient();
	return useMutation<BrandResponse, Error, { id: string; body: UpdateBrandRequest }>({
		mutationFn: ({ id, body }) => brands.update(id, body),
		onSuccess: (_data, { id }) => {
			void queryClient.invalidateQueries({ queryKey: queryKeys.brand(id) });
			void queryClient.invalidateQueries({ queryKey: queryKeys.brands() });
		},
	});
};

export const useDeleteBrandMutation = () => {
	const queryClient = useQueryClient();
	return useMutation<void, Error, string>({
		mutationFn: (id) => brands._delete(id),
		onSuccess: (_data, brandId) => {
			void queryClient.removeQueries({
				queryKey: queryKeys.brand(brandId),
			});
			void queryClient.invalidateQueries({
				queryKey: queryKeys.brands(),
			});
			void queryClient.invalidateQueries({
				queryKey: queryKeys.brandContents({ brandId }),
			});
		},
	});
};
