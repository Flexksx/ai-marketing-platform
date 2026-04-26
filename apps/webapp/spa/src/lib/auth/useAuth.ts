import type {
	LoginRequest,
	LoginResponse,
} from "@ai-marketing-platform/platform-api-client";
import { useQueryClient } from "@tanstack/vue-query";
import { computed, type InjectionKey, inject, provide, unref } from "vue";

import { authTokenStorage } from "./authTokenStorage";
import {
	useSignInMutation,
	useSignOutMutation,
	useSignUpMutation,
} from "./mutations";
import { useAuthSession } from "./queries";
import { queryKeys } from "./queryKeys";
import type { AuthSession } from "./types";

function buildAuth() {
	const queryClient = useQueryClient();
	const session = useAuthSession();

	const persistSession = (data: LoginResponse) => {
		if (!data.token) {
			return;
		}
		authTokenStorage.set(data.token);
		void queryClient.setQueryData<AuthSession>(queryKeys.authSession(), {
			accessToken: data.token,
		});
	};

	const signInMutation = useSignInMutation({
		onSuccess: persistSession,
	});
	const signUpMutation = useSignUpMutation({
		onSuccess: persistSession,
	});
	const signOutMutation = useSignOutMutation({
		onSettled: () => {
			authTokenStorage.clear();
			void queryClient.setQueryData<AuthSession>(queryKeys.authSession(), null);
		},
	});

	const isAuthenticated = computed(() => !!unref(session.data)?.accessToken);

	return {
		session,
		isAuthenticated,
		signIn: (credentials: LoginRequest) =>
			signInMutation.mutateAsync(credentials),
		signUp: (credentials: LoginRequest) =>
			signUpMutation.mutateAsync(credentials),
		signOut: () => signOutMutation.mutateAsync(),
		isLoggingIn: signInMutation.isPending,
		isRegistering: signUpMutation.isPending,
		isLoggingOut: signOutMutation.isPending,
		isLoginError: signInMutation.isError,
		loginError: signInMutation.error,
		isRegisterError: signUpMutation.isError,
		registerError: signUpMutation.error,
	};
}

export type UseAuth = ReturnType<typeof buildAuth>;

export const authKey: InjectionKey<UseAuth> = Symbol("auth");

export function useAuthProvider() {
	const context = buildAuth();
	provide(authKey, context);
	return context;
}

export function useAuth(): UseAuth {
	const context = inject(authKey);
	if (!context) {
		throw new Error(
			"useAuth() must be used under a parent that called useAuthProvider()",
		);
	}
	return context;
}
