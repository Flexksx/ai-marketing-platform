import {
	getAuthentication,
	type LoginRequest,
	type LoginResponse,
} from "@ai-marketing-platform/platform-api-client";
import { useQuery } from "@tanstack/vue-query";

import { authQueryKeys } from "./queryKeys";
import type { AuthSession } from "./types";
import { getAccessToken } from "./useLocalStorageToken";

const authApi = getAuthentication();

/**
 * All HTTP to auth endpoints goes through this module. Mutations call these, never the client directly.
 */
export function queryAuthLoginWithCredentials(
	credentials: LoginRequest,
): Promise<LoginResponse> {
	return authApi.login(credentials);
}

export function queryAuthRegisterWithCredentials(
	credentials: LoginRequest,
): Promise<LoginResponse> {
	return authApi.register(credentials);
}

export function queryAuthLogout(): Promise<void> {
	return authApi.logout();
}

function readSessionFromStorage(): AuthSession {
	const t = getAccessToken();
	if (!t) {
		return null;
	}
	return { accessToken: t };
}

export function useAuthSession() {
	return useQuery<AuthSession>({
		queryKey: authQueryKeys.session(),
		queryFn: readSessionFromStorage,
		initialData: readSessionFromStorage,
		staleTime: Number.POSITIVE_INFINITY,
	});
}
