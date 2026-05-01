import { browser } from '$app/environment';
import axios from 'axios';

function parseCookies(cookieString: string): Record<string, string> {
	return cookieString
		.split(';')
		.map((cookie) => cookie.trim())
		.filter((cookie) => cookie.length > 0)
		.reduce(
			(acc, cookie) => {
				const [key, ...valueParts] = cookie.split('=');
				const value = valueParts.join('=');
				if (key) {
					acc[decodeURIComponent(key)] = decodeURIComponent(value || '');
				}
				return acc;
			},
			{} as Record<string, string>
		);
}

if (browser) {
	axios.interceptors.request.use((config) => {
		if (!config.headers.Authorization) {
			const cookies = parseCookies(document.cookie || '');
			const authCookieKey = Object.keys(cookies).find(
				(k) => k.startsWith('sb-') && k.endsWith('-auth-token')
			);

			if (authCookieKey) {
				try {
					const session = JSON.parse(cookies[authCookieKey]);
					const token = session[0];
					if (token) config.headers.Authorization = `Bearer ${token}`;
				} catch (e) {
					/* ignore */
				}
			}
		}

		return config;
	});
}
