import type { RequestHandler } from './$types';
import { env as privateEnv } from '$env/dynamic/private';

const BACKEND_URL = (privateEnv.BACKEND_URL ?? 'http://localhost:8000').replace(/\/$/, '');

const HOP_BY_HOP_HEADERS = new Set([
	'connection',
	'keep-alive',
	'proxy-authenticate',
	'proxy-authorization',
	'te',
	'trailers',
	'transfer-encoding',
	'upgrade',
	'host',
	'content-length'
]);

async function proxyRequest(event: Parameters<RequestHandler>[0]): Promise<Response> {
	const targetUrl = `${BACKEND_URL}/${event.params.path}${event.url.search}`;

	const {
		data: { session }
	} = await event.locals.supabase.auth.getSession();

	const headers = new Headers();
	for (const [key, value] of event.request.headers) {
		if (!HOP_BY_HOP_HEADERS.has(key.toLowerCase())) {
			headers.set(key, value);
		}
	}

	if (session?.access_token) {
		headers.set('Authorization', `Bearer ${session.access_token}`);
	}

	const hasBody = ['POST', 'PUT', 'PATCH'].includes(event.request.method);

	const response = await fetch(targetUrl, {
		method: event.request.method,
		headers,
		...(hasBody ? { body: event.request.body, duplex: 'half' } : {})
	});

	const responseHeaders = new Headers();
	for (const [key, value] of response.headers) {
		if (!HOP_BY_HOP_HEADERS.has(key.toLowerCase())) {
			responseHeaders.set(key, value);
		}
	}

	return new Response(response.body, {
		status: response.status,
		statusText: response.statusText,
		headers: responseHeaders
	});
}

export const GET: RequestHandler = proxyRequest;
export const POST: RequestHandler = proxyRequest;
export const PUT: RequestHandler = proxyRequest;
export const PATCH: RequestHandler = proxyRequest;
export const DELETE: RequestHandler = proxyRequest;
