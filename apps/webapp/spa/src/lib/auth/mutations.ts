import type { LoginRequest, LoginResponse } from "@ai-marketing-platform/platform-api-client";
import { useMutation, type UseMutationOptions } from "@tanstack/vue-query";

import {
	queryAuthLoginWithCredentials,
	queryAuthLogout,
	queryAuthRegisterWithCredentials,
} from "./queries";

export type AuthJwtTokenMutationOptions = Omit<
	UseMutationOptions<LoginResponse, Error, LoginRequest, unknown>,
	"mutationFn"
>;

export type ResetJwtTokenMutationOptions = Omit<
	UseMutationOptions<void, Error, void, unknown>,
	"mutationFn"
>;

export function useAuthJwtTokenWithCredentials(
	options?: AuthJwtTokenMutationOptions,
) {
	return useMutation<LoginResponse, Error, LoginRequest, unknown>({
		...options,
		mutationFn: (body) => queryAuthLoginWithCredentials(body),
	});
}

export function useAuthRegisterWithCredentials(
	options?: AuthJwtTokenMutationOptions,
) {
	return useMutation<LoginResponse, Error, LoginRequest, unknown>({
		...options,
		mutationFn: (body) => queryAuthRegisterWithCredentials(body),
	});
}

export function useResetJwtToken(options?: ResetJwtTokenMutationOptions) {
	return useMutation<void, Error, void, unknown>({
		...options,
		mutationFn: () => queryAuthLogout(),
	});
}
