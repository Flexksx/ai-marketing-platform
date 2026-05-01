import { fail, redirect } from '@sveltejs/kit';
import {
	getErrorMessage,
	normalizeSupabaseError,
	SUPABASE_AUTH_ERROR_MESSAGES,
	SUPABASE_AUTH_ERRORS,
	validateEmail,
	validatePasswordStrength
} from '$lib/supabase/error-codes';

import type { Actions } from './$types';

export const actions: Actions = {
	signup: async ({ request, locals: { supabase } }) => {
		const formData = await request.formData();
		const email = formData.get('email') as string;
		const password = formData.get('password') as string;
		const confirmPassword = formData.get('confirmPassword') as string;

		// Check for missing fields
		if (!email || !password || !confirmPassword) {
			return fail(400, {
				error: getErrorMessage(SUPABASE_AUTH_ERRORS.MISSING_FIELDS)
			});
		}

		// Validate email format
		if (!validateEmail(email)) {
			return fail(400, {
				error: getErrorMessage(SUPABASE_AUTH_ERRORS.EMAIL_INVALID_FORMAT)
			});
		}

		// Check if passwords match
		if (password !== confirmPassword) {
			return fail(400, {
				error: getErrorMessage(SUPABASE_AUTH_ERRORS.PASSWORDS_DO_NOT_MATCH)
			});
		}

		// Validate password strength
		const passwordValidation = validatePasswordStrength(password);
		if (!passwordValidation.isValid) {
			return fail(400, {
				error: getErrorMessage(passwordValidation.errorCode!)
			});
		}

		const { error } = await supabase.auth.signUp({ email, password });
		if (error) {
			const normalizedError = normalizeSupabaseError(error.message);
			const errorMessage = getErrorMessage(normalizedError);
			return fail(400, {
				error: errorMessage
			});
		} else {
			// Return success message instead of redirecting
			return {
				success: true,
				message: SUPABASE_AUTH_ERROR_MESSAGES.SIGNUP_SUCCESS
			};
		}
	},
	login: async ({ request, locals: { supabase } }) => {
		const formData = await request.formData();
		const email = formData.get('email') as string;
		const password = formData.get('password') as string;

		if (!email || !password) {
			return fail(400, {
				error: getErrorMessage(SUPABASE_AUTH_ERRORS.MISSING_FIELDS)
			});
		}

		const { error } = await supabase.auth.signInWithPassword({
			email,
			password
		});
		if (error) {
			const normalizedError = normalizeSupabaseError(error.message);
			const errorMessage = getErrorMessage(normalizedError);
			return fail(400, {
				error: errorMessage
			});
		} else {
			redirect(303, '/');
		}
	}
};
