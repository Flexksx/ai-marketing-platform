import type { LoginRequest, LoginResponse } from "@ai-marketing-platform/platform-api-client";
import { useQueryClient } from "@tanstack/vue-query";
import { computed, inject, unref, type InjectionKey } from "vue";

import {
	useAuthJwtTokenWithCredentials,
	useAuthRegisterWithCredentials,
	useResetJwtToken,
} from "./mutations";
import { useAuthSession } from "./queries";
import { authQueryKeys } from "./queryKeys";
import type { AuthSession } from "./types";
import { clearAccessToken, setAccessToken } from "./useLocalStorageToken";

function createAuth() {
	const queryClient = useQueryClient();

	const session = useAuthSession();

	const onAuthSuccess = (data: LoginResponse) => {
		if (!data.token) {
			return;
		}
		setAccessToken(data.token);
		void queryClient.setQueryData<AuthSession>(authQueryKeys.session(), {
			accessToken: data.token,
		});
	};

	const signInRequest = useAuthJwtTokenWithCredentials({
		onSuccess: onAuthSuccess,
	});

	const signUpRequest = useAuthRegisterWithCredentials({
		onSuccess: onAuthSuccess,
	});

	const signOutRequest = useResetJwtToken({
		onSettled: () => {
			clearAccessToken();
			void queryClient.setQueryData<AuthSession>(authQueryKeys.session(), null);
		},
	});

	const isAuthenticated = computed(
		() => !!unref(session.data)?.accessToken,
	);

	return {
		session,
		isAuthenticated,
		signIn: (credentials: LoginRequest) => signInRequest.mutateAsync(credentials),
		signUp: (credentials: LoginRequest) => signUpRequest.mutateAsync(credentials),
		signOut: () => signOutRequest.mutateAsync(),
		isLoggingIn: signInRequest.isPending,
		isRegistering: signUpRequest.isPending,
		isLoggingOut: signOutRequest.isPending,
		isLoginError: signInRequest.isError,
		loginError: signInRequest.error,
		isRegisterError: signUpRequest.isError,
		registerError: signUpRequest.error,
	};
}

export type UseAuth = ReturnType<typeof createAuth>;

export const authKey: InjectionKey<UseAuth> = Symbol("auth");

export function useAuth() {
	return inject(authKey) ?? createAuth();
}
