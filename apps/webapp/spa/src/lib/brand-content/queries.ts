import { getBrandContent } from "@ai-marketing-platform/platform-api-client";
import { useQuery } from "@tanstack/vue-query";
import { computed, type MaybeRefOrGetter, toValue } from "vue";
import { queryKeys } from "@/lib/queryKeys";
import type { QueryTuning } from "../queryTuning";

const brandContent = getBrandContent();

export const useBrandContentItemsQuery = (
	brandId: MaybeRefOrGetter<string | null | undefined>,
	tuning: QueryTuning = {},
) =>
	useQuery({
		...tuning,
		queryKey: computed(() =>
			queryKeys.brandContents({
				brandId: String(toValue(brandId) ?? ""),
			}),
		),
		queryFn: () => {
			const id = toValue(brandId);
			if (!id) {
				throw new Error("brandId is required");
			}
			return brandContent.search1(id);
		},
		enabled: computed(() => !!toValue(brandId)),
	});

export const useBrandContentItemQuery = (
	brandId: MaybeRefOrGetter<string | null | undefined>,
	contentId: MaybeRefOrGetter<string | null | undefined>,
	tuning: QueryTuning = {},
) =>
	useQuery({
		...tuning,
		queryKey: computed(() =>
			queryKeys.brandContent(String(toValue(contentId) ?? "")),
		),
		queryFn: () => {
			const b = toValue(brandId);
			const c = toValue(contentId);
			if (!b || !c) {
				throw new Error("brandId and contentId are required");
			}
			return brandContent.get1(b, c);
		},
		enabled: computed(() => !!toValue(brandId) && !!toValue(contentId)),
	});
