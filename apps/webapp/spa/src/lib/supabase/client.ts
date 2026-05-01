import { createBrowserClient } from '@supabase/ssr';
import { env as publicEnv } from '$env/dynamic/public';

const supabaseUrl = publicEnv.PUBLIC_SUPABASE_URL ?? '';
const supabaseKey = publicEnv.PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? '';

if (!supabaseUrl || !supabaseKey) {
	throw new Error(
		'Supabase environment variables are required. Please set PUBLIC_SUPABASE_URL and PUBLIC_SUPABASE_PUBLISHABLE_KEY. ' +
			'For local development, create a .dev.vars file in the project root. ' +
			'For production, set them in the Cloudflare Pages dashboard under Settings → Environment Variables. ' +
			"Check https://supabase.com/dashboard/project/_/settings/api for your project's URL and Key."
	);
}

export const supabase = createBrowserClient(supabaseUrl, supabaseKey);
