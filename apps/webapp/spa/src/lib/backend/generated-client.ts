/**
 * Configures the auto-generated hey-api axios client with the correct base URL
 * and Supabase auth token injection. Import this module once, early in the app
 * lifecycle (e.g. root +layout.ts), before any generated SDK calls are made.
 */
import { browser } from '$app/environment';
import { client } from '$lib/api/generated/client.gen';

const getBackendUrl = (): string => {
	const url =
		typeof window !== 'undefined'
			? import.meta.env.PUBLIC_BACKEND_URL || 'http://localhost:8000'
			: process.env.BACKEND_URL || process.env.PUBLIC_BACKEND_URL || 'http://localhost:8000';
	return url.replace(/\/$/, '');
};

function parseCookies(cookieString: string): Record<string, string> {
	return cookieString
		.split(';')
		.map((c) => c.trim())
		.filter(Boolean)
		.reduce(
			(acc, cookie) => {
				const [key, ...rest] = cookie.split('=');
				if (key) acc[decodeURIComponent(key)] = decodeURIComponent(rest.join('=') || '');
				return acc;
			},
			{} as Record<string, string>
		);
}

client.setConfig({ baseURL: getBackendUrl() });

if (browser) {
	client.instance.interceptors.request.use((config) => {
		if (!config.headers.Authorization) {
			const cookies = parseCookies(document.cookie || '');
			const authKey = Object.keys(cookies).find(
				(k) => k.startsWith('sb-') && k.endsWith('-auth-token')
			);
			if (authKey) {
				try {
					const session = JSON.parse(cookies[authKey]);
					const token = session[0];
					if (token) config.headers.Authorization = `Bearer ${token}`;
				} catch {
					/* ignore */
				}
			}
		}
		return config;
	});
}

export { client };
