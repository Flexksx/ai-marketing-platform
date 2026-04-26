import { type Ref, ref } from "vue";

const ACCESS_TOKEN_KEY = "access_token";

function readStoredToken(): string | null {
	if (typeof localStorage === "undefined") {
		return null;
	}
	return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export const isAuthenticated: Ref<boolean> = ref(!!readStoredToken());

export function getAccessToken(): string | null {
	return readStoredToken();
}

export function setAccessToken(token: string) {
	if (typeof localStorage === "undefined") {
		return;
	}
	localStorage.setItem(ACCESS_TOKEN_KEY, token);
	isAuthenticated.value = true;
}

export function clearAccessToken() {
	if (typeof localStorage === "undefined") {
		return;
	}
	localStorage.removeItem(ACCESS_TOKEN_KEY);
	isAuthenticated.value = false;
}
