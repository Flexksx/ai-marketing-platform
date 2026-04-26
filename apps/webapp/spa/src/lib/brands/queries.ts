import { getBrands } from "@ai-marketing-platform/platform-api-client";
import { useQuery } from "@tanstack/vue-query";
import { computed, type MaybeRefOrGetter, toValue } from "vue";
import { queryKeys } from "@/lib/queryKeys";
import type { QueryTuning } from "../queryTuning";

const brands = getBrands();

export const useBrandsListQuery = (tuning: QueryTuning = {}) =>
	useQuery({
		...tuning,
		queryKey: queryKeys.brands(),
		queryFn: () => brands.search(),
	});

export const useBrandDetailQuery = (
	brandId: MaybeRefOrGetter<string | null | undefined>,
	tuning: QueryTuning = {},
) =>
	useQuery({
		...tuning,
		queryKey: computed(() => queryKeys.brand(String(toValue(brandId) ?? ""))),
		queryFn: () => {
			const id = toValue(brandId);
			if (!id) {
				throw new Error("brandId is required");
			}
			return brands.get(id);
		},
		enabled: computed(() => !!toValue(brandId)),
	});
