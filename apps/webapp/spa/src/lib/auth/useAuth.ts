import type { LoginResponse } from "@ai-marketing-platform/platform-api-client";
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

	const signIn = useSignInMutation({ onSuccess: persistSession });
	const signUp = useSignUpMutation({ onSuccess: persistSession });
	const signOut = useSignOutMutation({
		onSettled: () => {
			authTokenStorage.clear();
			void queryClient.setQueryData<AuthSession>(queryKeys.authSession(), null);
		},
	});

	return {
		session,
		isAuthenticated: computed(() => !!unref(session.data)?.accessToken),
		signIn,
		signUp,
		signOut,
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
