import { useQuery } from "@tanstack/vue-query";
import { queryKeys } from "@/lib/queryKeys";
import { authTokenStorage } from "./authTokenStorage";
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
		queryKey: queryKeys.auth.session(),
		queryFn: readSessionFromStorage,
		initialData: readSessionFromStorage,
		staleTime: Number.POSITIVE_INFINITY,
	});
}
