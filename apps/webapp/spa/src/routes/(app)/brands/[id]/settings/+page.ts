import type { PageLoad } from './$types';
import { BrandsApi } from '$lib/api/generated/apis/BrandsApi';
import { openApiConfiguration } from '$lib/backend/generated-client';
import { queryKeys } from '$lib/resources/queryKeys';

export const load: PageLoad = async ({ params, parent }) => {
	const { queryClient } = await parent();
	await queryClient.prefetchQuery({
		queryKey: queryKeys.brand(params.id),
		queryFn: () => new BrandsApi(openApiConfiguration).brandsGet({ brandId: params.id })
	});
};
