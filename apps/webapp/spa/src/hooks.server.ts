import { type Handle, type HandleServerError } from '@sveltejs/kit';
import { paraglideMiddleware } from '$lib/paraglide/server';
import { createServerClient } from '@supabase/ssr';
import { env as publicEnv } from '$env/dynamic/public';
import { env as privateEnv } from '$env/dynamic/private';
import { redirect } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';
import { logRequest, logger } from '$lib/server/utils/logger';

const handleParaglide: Handle = ({ event, resolve }) =>
	paraglideMiddleware(event.request, ({ request, locale }) => {
		event.request = request;
		return resolve(event, {
			transformPageChunk: ({ html }) => html.replace('%paraglide.lang%', locale)
		});
	});

const supabaseSSR: Handle = async ({ event, resolve }) => {
	const supabaseUrl = publicEnv.PUBLIC_SUPABASE_URL ?? '';
	const supabaseKey = publicEnv.PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? '';

	event.locals.supabase = createServerClient(supabaseUrl, supabaseKey, {
		cookies: {
			getAll: () => event.cookies.getAll(),
			setAll: (cookiesToSet) => {
				cookiesToSet.forEach(({ name, value, options }) => {
					event.cookies.set(name, value, {
						...options,
						path: '/'
					});
				});
			}
		}
	});

	event.locals.safeGetSession = async () => {
		const {
			data: { user },
			error
		} = await event.locals.supabase.auth.getUser();
		if (error || !user) return { session: null, user: null };

		const {
			data: { session }
		} = await event.locals.supabase.auth.getSession();

		return { session, user };
	};

	return resolve(event, {
		filterSerializedResponseHeaders(name) {
			return name === 'content-range' || name === 'x-supabase-api-version';
		}
	});
};

const authGuard: Handle = async ({ event, resolve }) => {
	const { session, user } = await event.locals.safeGetSession();
	event.locals.session = session;
	event.locals.user = user;

	const isPublic = event.url.pathname === '/login' || event.url.pathname === '/register';
	const isApi = event.url.pathname.startsWith('/api');

	if (!session && !isPublic) {
		if (isApi) {
			return new Response(JSON.stringify({ error: 'Unauthorized' }), {
				status: 401,
				headers: { 'Content-Type': 'application/json' }
			});
		}
		throw redirect(303, '/login');
	}

	if (session && event.url.pathname === '/login') {
		throw redirect(303, '/');
	}
	return resolve(event);
};

// src/hooks.server.ts

const handleBackendProxy: Handle = async ({ event, resolve }) => {
	if (event.url.pathname.startsWith('/api')) {
		const backendUrl = privateEnv.BACKEND_URL || 'http://localhost:8000';
		const path = event.url.pathname.replace(/^\/api/, '');
		const targetUrl = `${backendUrl}${path}${event.url.search}`;

		logger.debug(
			{ method: event.request.method, path: event.url.pathname, targetUrl },
			'Proxying request to backend'
		);

		const headers = new Headers(event.request.headers);
		headers.delete('host');
		headers.delete('connection');
		headers.delete('content-length');

		const session = event.locals.session;
		if (session?.access_token) {
			headers.set('Authorization', `Bearer ${session.access_token}`);
		}

		const hasBody =
			['POST', 'PUT', 'PATCH', 'DELETE'].includes(event.request.method) && event.request.body;

		try {
			const response = await fetch(targetUrl, {
				method: event.request.method,
				headers,
				...(hasBody ? { body: event.request.body, duplex: 'half' } : {})
			});

			logger.debug({ status: response.status }, 'Backend response received');

			return new Response(response.body, {
				status: response.status,
				statusText: response.statusText,
				headers: response.headers
			});
		} catch (err) {
			logger.error(
				{ error: err instanceof Error ? err.message : String(err) },
				'Proxy request failed'
			);
			return new Response(JSON.stringify({ error: 'Backend unavailable' }), {
				status: 502,
				headers: { 'Content-Type': 'application/json' }
			});
		}
	}

	return resolve(event);
};

const handleRequestTiming: Handle = async ({ event, resolve }) => {
	const start = performance.now();

	const requestInfo = {
		method: event.request.method,
		path: event.url.pathname,
		url: event.url.href,
		query: Object.fromEntries(event.url.searchParams),
		userAgent: event.request.headers.get('user-agent')?.substring(0, 50),
		ip: event.getClientAddress()
	};

	logger.info(requestInfo, `➡️  ${event.request.method} ${event.url.pathname}`);

	const response = await resolve(event);
	const duration = performance.now() - start;
	const statusCode = response.status || 200;

	logRequest(event.request.method, event.url.pathname, statusCode, duration, {
		url: event.url.href,
		query: Object.fromEntries(event.url.searchParams)
	});

	return response;
};

export const handle: Handle = sequence(
	handleParaglide,
	supabaseSSR,
	authGuard,
	handleBackendProxy,
	handleRequestTiming
);

export const handleError: HandleServerError = ({ error, event }) => {
	const errorMessage = error instanceof Error ? error.message : String(error);

	logger.error(
		{
			error: errorMessage,
			stack: error instanceof Error ? error.stack : undefined,
			url: event.url.href,
			path: event.url.pathname,
			method: event.request.method
		},
		'Server error'
	);

	const isProduction = process.env.NODE_ENV === 'production';

	if (isProduction) {
		return {
			message: 'An unexpected error occurred. Please try again.'
		};
	}

	return {
		message: errorMessage
	};
};
