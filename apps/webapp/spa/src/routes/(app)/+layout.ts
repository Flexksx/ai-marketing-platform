export const ssr = false;

import { redirect } from '@sveltejs/kit';
import { supabase } from '$lib/supabase/client';

const SESSION_GET_MS = 3000;

async function getSessionSafe() {
	const sessionPromise = supabase.auth.getSession();
	const timeout = new Promise<{ data: { session: null } }>((resolve) =>
		setTimeout(() => resolve({ data: { session: null } }), SESSION_GET_MS)
	);
	try {
		const result = await Promise.race([sessionPromise, timeout]);
		return result.data.session;
	} catch {
		return null;
	}
}

export const load = async ({ depends }) => {
	depends('supabase:auth');

	const session = await getSessionSafe();
	if (!session) {
		throw redirect(303, '/login');
	}
	return { session, user: session.user };
};
