import type { LoginRequest, LoginResponse } from "@ai-marketing-platform/platform-api-client";
import { getAuthRestController } from "@ai-marketing-platform/platform-api-client";
import { useMutation, useQueryClient } from "@tanstack/vue-query";

import { authQueryKeys } from "./queryKeys";
import { clearAccessToken, setAccessToken } from "./useLocalStorageToken";

const auth = getAuthRestController();

export function useLogin() {
	return useMutation<LoginResponse, Error, LoginRequest>({
		mutationFn: (body) => auth.login(body),
		onSuccess: (data) => {
			if (data.token) {
				setAccessToken(data.token);
			}
		},
	});
}

export function useLogout() {
	const queryClient = useQueryClient();

	return useMutation({
		mutationFn: () => auth.logout(),
		onSettled: () => {
			clearAccessToken();
			void queryClient.removeQueries({ queryKey: authQueryKeys.root() });
		},
	});
}
