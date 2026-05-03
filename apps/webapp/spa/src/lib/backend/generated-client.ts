import { Configuration } from '$lib/api/generated';

export const openApiConfiguration = new Configuration({
	basePath: '/api',
	headers: {
		'Content-Type': 'application/json'
	}
});
