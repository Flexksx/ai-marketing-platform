import { browser } from '$app/environment';
import { goto } from '$app/navigation';

const GOTO_FALLBACK_MS = 1000;

export async function navigate(path: string): Promise<void> {
	if (!browser) return;
	let fallbackFired = false;
	const timeoutId = setTimeout(() => {
		fallbackFired = true;
		window.location.assign(path);
	}, GOTO_FALLBACK_MS);
	try {
		await goto(path, { invalidateAll: false });
		if (!fallbackFired) clearTimeout(timeoutId);
	} catch {
		if (!fallbackFired) {
			clearTimeout(timeoutId);
			window.location.assign(path);
		}
	}
}
