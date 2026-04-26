const ACCESS_TOKEN_KEY = "access_token";

function isBrowserStorageAvailable(): boolean {
	return typeof localStorage !== "undefined";
}

export const authTokenStorage = {
	get(): string | null {
		if (!isBrowserStorageAvailable()) {
			return null;
		}
		return localStorage.getItem(ACCESS_TOKEN_KEY);
	},
	set(token: string): void {
		if (!isBrowserStorageAvailable()) {
			return;
		}
		localStorage.setItem(ACCESS_TOKEN_KEY, token);
	},
	clear(): void {
		if (!isBrowserStorageAvailable()) {
			return;
		}
		localStorage.removeItem(ACCESS_TOKEN_KEY);
	},
} as const;
