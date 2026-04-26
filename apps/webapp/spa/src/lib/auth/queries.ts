import { useQuery } from "@tanstack/vue-query";

import { authTokenStorage } from "./authTokenStorage";
import { queryKeys } from "./queryKeys";
import type { AuthSession } from "./types";

function readSessionFromStorage(): AuthSession {
	const token = authTokenStorage.get();
	if (!token) {
		return null;
	}
	return { accessToken: token };
}

export function useAuthSession() {
	return useQuery<AuthSession>({
		queryKey: queryKeys.authSession(),
		queryFn: readSessionFromStorage,
		initialData: readSessionFromStorage,
		staleTime: Number.POSITIVE_INFINITY,
	});
}
