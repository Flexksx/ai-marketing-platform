import {
	getAuthentication,
	type LoginRequest,
	type LoginResponse,
} from "@ai-marketing-platform/platform-api-client";
import { type UseMutationOptions, useMutation } from "@tanstack/vue-query";

const auth = getAuthentication();

export type CredentialsMutationOptions = Omit<
	UseMutationOptions<LoginResponse, Error, LoginRequest, unknown>,
	"mutationFn"
>;

export type SignOutMutationOptions = Omit<
	UseMutationOptions<void, Error, void, unknown>,
	"mutationFn"
>;

export function useSignInMutation(options?: CredentialsMutationOptions) {
	return useMutation<LoginResponse, Error, LoginRequest, unknown>({
		...options,
		mutationFn: (body) => auth.login(body),
	});
}

export function useSignUpMutation(options?: CredentialsMutationOptions) {
	return useMutation<LoginResponse, Error, LoginRequest, unknown>({
		...options,
		mutationFn: (body) => auth.register(body),
	});
}

export function useSignOutMutation(options?: SignOutMutationOptions) {
	return useMutation<void, Error, void, unknown>({
		...options,
		mutationFn: () => auth.logout(),
	});
}
