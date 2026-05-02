export const ssr = false;

import { openApiConfiguration } from '$lib/backend/generated-client';
import { BrandsApi } from '$lib/api/generated/apis/BrandsApi';
import { redirect } from '@sveltejs/kit';

export const load = async () => {
	const api = new BrandsApi(openApiConfiguration);
	const brands = await api.brandsSearch({ offset: 0, limit: 1 });

	if (brands.length === 0) {
		throw redirect(303, '/brands/create');
	}

	throw redirect(303, `/brands/${brands[0].id}`);
};
