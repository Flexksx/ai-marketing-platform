import type { Handle } from '@sveltejs/kit';
import { createServerClient } from '@supabase/ssr';
import { env as publicEnv } from '$env/dynamic/public';

export const handle: Handle = async ({ event, resolve }) => {
	event.locals.supabase = createServerClient(
		publicEnv.PUBLIC_SUPABASE_URL ?? '',
		publicEnv.PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? '',
		{
			cookies: {
				getAll: () => event.cookies.getAll(),
				setAll: (cookiesToSet) => {
					cookiesToSet.forEach(({ name, value, options }) => {
						event.cookies.set(name, value, { ...options, path: '/' });
					});
				}
			}
		}
	);

	return resolve(event);
};
