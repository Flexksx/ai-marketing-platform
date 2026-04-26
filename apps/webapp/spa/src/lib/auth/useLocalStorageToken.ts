const ACCESS_TOKEN_KEY = "access_token";

function readStoredToken(): string | null {
	if (typeof localStorage === "undefined") {
		return null;
	}
	return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getAccessToken(): string | null {
	return readStoredToken();
}

export function setAccessToken(token: string) {
	if (typeof localStorage === "undefined") {
		return;
	}
	localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function clearAccessToken() {
	if (typeof localStorage === "undefined") {
		return;
	}
	localStorage.removeItem(ACCESS_TOKEN_KEY);
}
