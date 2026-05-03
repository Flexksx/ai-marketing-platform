import { createBrowserClient } from '@supabase/ssr';
import { env as publicEnv } from '$env/dynamic/public';

const supabaseUrl = publicEnv.PUBLIC_SUPABASE_URL ?? '';
const supabaseKey = publicEnv.PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? '';

if (!supabaseUrl || !supabaseKey) {
	throw new Error(
		'Supabase environment variables are required. Please set PUBLIC_SUPABASE_URL and PUBLIC_SUPABASE_PUBLISHABLE_KEY in your environment.'
	);
}

export const supabase = createBrowserClient(supabaseUrl, supabaseKey);
