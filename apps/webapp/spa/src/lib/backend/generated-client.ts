/**
 * Shared OpenAPI Generator (typescript-fetch) configuration: camelCase in TS,
 * snake_case on the wire via *ToJSON / *FromJSON.
 *
 * Import `openApiConfiguration` when constructing generated *Api classes.
 */
import { browser } from '$app/environment';
import { Configuration, type Middleware } from '$lib/api/generated';

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

function bearerFromBrowserCookies(): string | undefined {
	const cookies = parseCookies(document.cookie || '');
	const authKey = Object.keys(cookies).find((k) => k.startsWith('sb-') && k.endsWith('-auth-token'));
	if (!authKey) return undefined;
	try {
		const session = JSON.parse(cookies[authKey]);
		const token = session[0];
		return typeof token === 'string' ? token : undefined;
	} catch {
		return undefined;
	}
}

const authMiddleware: Middleware = {
	pre: async ({ url, init }) => {
		if (!browser) return undefined;
		const token = bearerFromBrowserCookies();
		if (!token) return undefined;
		const headers = new Headers(init.headers);
		if (!headers.has('Authorization')) {
			headers.set('Authorization', `Bearer ${token}`);
		}
		return { url, init: { ...init, headers } };
	}
};

export const openApiConfiguration = new Configuration({
	basePath: getBackendUrl(),
	headers: {
		'Content-Type': 'application/json'
	},
	middleware: browser ? [authMiddleware] : []
});
