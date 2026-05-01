import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const SIDEBAR_STORAGE_KEY = 'sidebar:state';

const createSidebarStore = () => {
	const { subscribe, set, update } = writable<boolean>(true);

	return {
		subscribe,
		set: (open: boolean) => {
			if (browser) {
				localStorage.setItem(SIDEBAR_STORAGE_KEY, JSON.stringify(open));
			}
			set(open);
		},
		init: () => {
			if (browser) {
				const stored = localStorage.getItem(SIDEBAR_STORAGE_KEY);
				if (stored !== null) {
					try {
						const open = JSON.parse(stored) as boolean;
						set(open);
					} catch {
						set(true);
					}
				} else {
					set(true);
				}
			}
		},
		toggle: () => {
			update((open) => {
				const newValue = !open;
				if (browser) {
					localStorage.setItem(SIDEBAR_STORAGE_KEY, JSON.stringify(newValue));
				}
				return newValue;
			});
		}
	};
};

export const sidebarStore = createSidebarStore();
