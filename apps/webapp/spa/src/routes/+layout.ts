import { QueryClient } from '@tanstack/svelte-query';
import { browser } from '$app/environment';

export const ssr = false;

let browserQueryClient: QueryClient;

function makeQueryClient() {
	return new QueryClient({
		defaultOptions: {
			queries: {
				staleTime: 60 * 1000,
				gcTime: 2 * 60 * 1000,
				retry: 2,
				refetchOnWindowFocus: false
			},
			mutations: {
				retry: 1
			}
		}
	});
}

function getQueryClient() {
	if (browser) {
		return (browserQueryClient ??= makeQueryClient());
	}
	return makeQueryClient();
}

export const load = async () => {
	const queryClient = getQueryClient();

	return {
		queryClient
	};
};
