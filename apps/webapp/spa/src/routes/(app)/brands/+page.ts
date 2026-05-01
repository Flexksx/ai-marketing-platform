export const ssr = false;

import { BrandEndpoints } from '$lib/api/brands/BrandEndpoints';
import { redirect } from '@sveltejs/kit';

export const load = async () => {
	const brands = await BrandEndpoints.list({ offset: 0, limit: 1 });

	if (brands.length === 0) {
		throw redirect(303, '/brands/create');
	}

	throw redirect(303, `/brands/${brands[0].id}`);
};
