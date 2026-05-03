import { supabase } from '$lib/supabase/client';
import {
	getErrorMessage,
	normalizeSupabaseError,
	SUPABASE_AUTH_ERROR_MESSAGES,
	SUPABASE_AUTH_ERRORS,
	validateEmail,
	validatePasswordStrength
} from '$lib/supabase/error-codes';

export type AuthFormResult =
	| { ok: true; redirect?: string }
	| { ok: true; success: true; message: string }
	| { ok: false; error: string };

export async function signupWithEmailPassword(
	email: string,
	password: string,
	confirmPassword: string
): Promise<AuthFormResult> {
	if (!email || !password || !confirmPassword) {
		return { ok: false, error: getErrorMessage(SUPABASE_AUTH_ERRORS.MISSING_FIELDS) };
	}
	if (!validateEmail(email)) {
		return { ok: false, error: getErrorMessage(SUPABASE_AUTH_ERRORS.EMAIL_INVALID_FORMAT) };
	}
	if (password !== confirmPassword) {
		return { ok: false, error: getErrorMessage(SUPABASE_AUTH_ERRORS.PASSWORDS_DO_NOT_MATCH) };
	}
	const passwordValidation = validatePasswordStrength(password);
	if (!passwordValidation.isValid) {
		return { ok: false, error: getErrorMessage(passwordValidation.errorCode!) };
	}

	const { error } = await supabase.auth.signUp({ email, password });
	if (error) {
		const normalizedError = normalizeSupabaseError(error.message);
		return { ok: false, error: getErrorMessage(normalizedError) };
	}
	return {
		ok: true,
		success: true,
		message: SUPABASE_AUTH_ERROR_MESSAGES.SIGNUP_SUCCESS
	};
}

export async function loginWithEmailPassword(
	email: string,
	password: string
): Promise<AuthFormResult> {
	if (!email || !password) {
		return { ok: false, error: getErrorMessage(SUPABASE_AUTH_ERRORS.MISSING_FIELDS) };
	}

	const { error } = await supabase.auth.signInWithPassword({ email, password });
	if (error) {
		const normalizedError = normalizeSupabaseError(error.message);
		return { ok: false, error: getErrorMessage(normalizedError) };
	}
	return { ok: true, redirect: '/' };
}
