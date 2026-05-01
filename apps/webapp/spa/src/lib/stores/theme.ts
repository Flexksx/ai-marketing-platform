import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type Theme = 'light' | 'dark' | 'system';

const createThemeStore = () => {
	const { subscribe, set } = writable<Theme>('system');

	return {
		subscribe,
		set: (theme: Theme) => {
			if (browser) {
				localStorage.setItem('theme', theme);
				applyTheme(theme);
			}
			set(theme);
		},
		init: () => {
			if (browser) {
				const stored = localStorage.getItem('theme') as Theme;
				const theme = stored || 'system';
				set(theme);
				applyTheme(theme);
			}
		}
	};
};

function applyTheme(theme: Theme) {
	if (!browser) return;

	const root = document.documentElement;

	if (theme === 'system') {
		const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		root.classList.toggle('dark', prefersDark);
	} else {
		root.classList.toggle('dark', theme === 'dark');
	}
}

export const theme = createThemeStore();

if (browser) {
	window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
		const currentTheme = localStorage.getItem('theme') as Theme;
		if (!currentTheme || currentTheme === 'system') {
			document.documentElement.classList.toggle('dark', e.matches);
		}
	});
}
