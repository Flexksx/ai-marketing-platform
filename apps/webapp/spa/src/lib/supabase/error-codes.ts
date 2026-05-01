export const SUPABASE_AUTH_ERRORS = {
	// Signup errors (actual Supabase error codes)
	EMAIL_ADDRESS_INVALID: 'email_address_invalid',
	WEAK_PASSWORD: 'weak_password',
	SIGNUP_DISABLED: 'signup_disabled',
	EMAIL_PROVIDER_DISABLED: 'email_provider_disabled',
	VALIDATION_FAILED: 'validation_failed',

	// Login errors
	INVALID_CREDENTIALS: 'invalid_credentials',
	EMAIL_NOT_CONFIRMED: 'email_not_confirmed',
	USER_NOT_FOUND: 'user_not_found',
	USER_BANNED: 'user_banned',
	OVER_REQUEST_RATE_LIMIT: 'over_request_rate_limit',

	// Custom validation errors
	PASSWORD_TOO_SHORT: 'password_too_short',
	PASSWORD_TOO_WEAK: 'password_too_weak',
	EMAIL_INVALID_FORMAT: 'email_invalid_format',
	PASSWORDS_DO_NOT_MATCH: 'passwords_do_not_match',
	MISSING_FIELDS: 'missing_fields',

	// General errors
	UNEXPECTED_FAILURE: 'unexpected_failure'
} as const;

export const VALIDATION_CONSTANTS = {
	MIN_PASSWORD_LENGTH: 8,
	WEAK_PASSWORDS: [
		'password',
		'123456',
		'qwerty',
		'abc123',
		'password123',
		'admin',
		'letmein',
		'welcome',
		'monkey',
		'dragon',
		'12345678',
		'password1',
		'qwerty123',
		'welcome123',
		'admin123',
		'test123',
		'user123',
		'guest',
		'root',
		'toor',
		'pass',
		'1234',
		'12345',
		'123456789',
		'1234567890',
		'iloveyou',
		'princess',
		'rockyou',
		'123123',
		'000000',
		'111111',
		'sunshine',
		'master',
		'hello',
		'freedom',
		'whatever',
		'qazwsx',
		'trustno1',
		'dragon',
		'baseball',
		'superman',
		'batman',
		'football',
		'hockey',
		'killer',
		'george',
		'sexy',
		'andrew',
		'charlie',
		'superman',
		'asshole',
		'fuckyou',
		'dallas',
		'jessica',
		'panties',
		'pepper',
		'1234',
		'azerty',
		'55555',
		'qwertyuiop',
		'asdfghjkl',
		'zxcvbnm',
		'qwertyuiopasdfghjklzxcvbnm'
	] as string[],
	EMAIL_REGEX:
		/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
} as const;

export const SUPABASE_AUTH_ERROR_MESSAGES = {
	// Signup error messages
	EMAIL_ADDRESS_INVALID: 'Please enter a valid email address. Test domains are not supported.',
	WEAK_PASSWORD: 'Password does not meet strength requirements. Please choose a stronger password.',
	SIGNUP_DISABLED: 'Account creation is currently disabled. Please contact support.',
	EMAIL_PROVIDER_DISABLED: 'Email signup is currently disabled. Please contact support.',
	VALIDATION_FAILED: 'Please check your input and try again.',

	// Login error messages
	INVALID_CREDENTIALS: 'Invalid email or password. Please check your credentials and try again.',
	EMAIL_NOT_CONFIRMED: 'Please check your email and click the confirmation link before signing in.',
	USER_NOT_FOUND: 'No account found with this email address. Please sign up instead.',
	USER_BANNED: 'Your account has been temporarily suspended. Please contact support.',
	OVER_REQUEST_RATE_LIMIT:
		'Too many login attempts. Please wait a few minutes before trying again.',

	// Custom validation error messages
	PASSWORD_TOO_SHORT: `Password must be at least ${VALIDATION_CONSTANTS.MIN_PASSWORD_LENGTH} characters long.`,
	PASSWORD_TOO_WEAK:
		'Password is too weak. Please choose a stronger password with a mix of letters, numbers, and symbols.',
	EMAIL_INVALID_FORMAT: 'Please enter a valid email address.',
	PASSWORDS_DO_NOT_MATCH:
		'Passwords do not match. Please make sure both password fields are identical.',
	MISSING_FIELDS: 'All fields are required. Please fill in all the information.',

	// General error messages
	UNEXPECTED_FAILURE: 'An unexpected error occurred. Please try again later.',

	// Success messages
	SIGNUP_SUCCESS:
		'Thank you! You should receive a confirmation email shortly. Please check your inbox and click the confirmation link to activate your account.',
	SIGNUP_EXISTING_USER:
		"If an account exists with this email, you'll receive a magic link to sign in."
} as const;

// Error mapping functions using maps instead of if-else statements
export const SIGNUP_ERROR_MAP = new Map<string, string>([
	[SUPABASE_AUTH_ERRORS.EMAIL_ADDRESS_INVALID, SUPABASE_AUTH_ERROR_MESSAGES.EMAIL_ADDRESS_INVALID],
	[SUPABASE_AUTH_ERRORS.WEAK_PASSWORD, SUPABASE_AUTH_ERROR_MESSAGES.WEAK_PASSWORD],
	[SUPABASE_AUTH_ERRORS.SIGNUP_DISABLED, SUPABASE_AUTH_ERROR_MESSAGES.SIGNUP_DISABLED],
	[
		SUPABASE_AUTH_ERRORS.EMAIL_PROVIDER_DISABLED,
		SUPABASE_AUTH_ERROR_MESSAGES.EMAIL_PROVIDER_DISABLED
	],
	[SUPABASE_AUTH_ERRORS.VALIDATION_FAILED, SUPABASE_AUTH_ERROR_MESSAGES.VALIDATION_FAILED],
	[SUPABASE_AUTH_ERRORS.PASSWORD_TOO_SHORT, SUPABASE_AUTH_ERROR_MESSAGES.PASSWORD_TOO_SHORT],
	[SUPABASE_AUTH_ERRORS.PASSWORD_TOO_WEAK, SUPABASE_AUTH_ERROR_MESSAGES.PASSWORD_TOO_WEAK],
	[SUPABASE_AUTH_ERRORS.EMAIL_INVALID_FORMAT, SUPABASE_AUTH_ERROR_MESSAGES.EMAIL_INVALID_FORMAT],
	[
		SUPABASE_AUTH_ERRORS.PASSWORDS_DO_NOT_MATCH,
		SUPABASE_AUTH_ERROR_MESSAGES.PASSWORDS_DO_NOT_MATCH
	],
	[SUPABASE_AUTH_ERRORS.MISSING_FIELDS, SUPABASE_AUTH_ERROR_MESSAGES.MISSING_FIELDS],
	[SUPABASE_AUTH_ERRORS.UNEXPECTED_FAILURE, SUPABASE_AUTH_ERROR_MESSAGES.UNEXPECTED_FAILURE]
]);

export const LOGIN_ERROR_MAP = new Map<string, string>([
	[SUPABASE_AUTH_ERRORS.INVALID_CREDENTIALS, SUPABASE_AUTH_ERROR_MESSAGES.INVALID_CREDENTIALS],
	[SUPABASE_AUTH_ERRORS.EMAIL_NOT_CONFIRMED, SUPABASE_AUTH_ERROR_MESSAGES.EMAIL_NOT_CONFIRMED],
	[SUPABASE_AUTH_ERRORS.USER_NOT_FOUND, SUPABASE_AUTH_ERROR_MESSAGES.USER_NOT_FOUND],
	[SUPABASE_AUTH_ERRORS.USER_BANNED, SUPABASE_AUTH_ERROR_MESSAGES.USER_BANNED],
	[
		SUPABASE_AUTH_ERRORS.OVER_REQUEST_RATE_LIMIT,
		SUPABASE_AUTH_ERROR_MESSAGES.OVER_REQUEST_RATE_LIMIT
	],
	[SUPABASE_AUTH_ERRORS.VALIDATION_FAILED, SUPABASE_AUTH_ERROR_MESSAGES.VALIDATION_FAILED],
	[SUPABASE_AUTH_ERRORS.UNEXPECTED_FAILURE, SUPABASE_AUTH_ERROR_MESSAGES.UNEXPECTED_FAILURE]
]);

// Validation helper functions
export function validateEmail(email: string): boolean {
	return VALIDATION_CONSTANTS.EMAIL_REGEX.test(email);
}

export function validatePasswordStrength(password: string): {
	isValid: boolean;
	errorCode?: string;
} {
	if (password.length < VALIDATION_CONSTANTS.MIN_PASSWORD_LENGTH) {
		return {
			isValid: false,
			errorCode: SUPABASE_AUTH_ERRORS.PASSWORD_TOO_SHORT
		};
	}

	if (VALIDATION_CONSTANTS.WEAK_PASSWORDS.includes(password.toLowerCase())) {
		return {
			isValid: false,
			errorCode: SUPABASE_AUTH_ERRORS.PASSWORD_TOO_WEAK
		};
	}

	// Additional strength checks
	const hasUpperCase = /[A-Z]/.test(password);
	const hasLowerCase = /[a-z]/.test(password);
	const hasNumbers = /\d/.test(password);
	const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

	const strengthScore = [hasUpperCase, hasLowerCase, hasNumbers, hasSpecialChar].filter(
		Boolean
	).length;

	if (strengthScore < 3) {
		return {
			isValid: false,
			errorCode: SUPABASE_AUTH_ERRORS.PASSWORD_TOO_WEAK
		};
	}

	return { isValid: true };
}

export function normalizeSupabaseError(errorMessage: string): string {
	const lowerMessage = errorMessage.toLowerCase();

	if (
		lowerMessage.includes('invalid login credentials') ||
		lowerMessage.includes('invalid credentials') ||
		lowerMessage.includes('wrong password')
	) {
		return SUPABASE_AUTH_ERRORS.INVALID_CREDENTIALS;
	}

	if (lowerMessage.includes('email not confirmed') || lowerMessage.includes('email confirmation')) {
		return SUPABASE_AUTH_ERRORS.EMAIL_NOT_CONFIRMED;
	}

	if (lowerMessage.includes('user not found') || lowerMessage.includes('no user found')) {
		return SUPABASE_AUTH_ERRORS.USER_NOT_FOUND;
	}

	if (
		lowerMessage.includes('too many requests') ||
		lowerMessage.includes('rate limit') ||
		lowerMessage.includes('rate_limit')
	) {
		return SUPABASE_AUTH_ERRORS.OVER_REQUEST_RATE_LIMIT;
	}

	if (lowerMessage.includes('user banned') || lowerMessage.includes('account suspended')) {
		return SUPABASE_AUTH_ERRORS.USER_BANNED;
	}

	if (lowerMessage.includes('email_address_invalid') || lowerMessage.includes('invalid email')) {
		return SUPABASE_AUTH_ERRORS.EMAIL_ADDRESS_INVALID;
	}

	if (lowerMessage.includes('weak_password') || lowerMessage.includes('weak password')) {
		return SUPABASE_AUTH_ERRORS.WEAK_PASSWORD;
	}

	if (lowerMessage.includes('validation_failed') || lowerMessage.includes('validation failed')) {
		return SUPABASE_AUTH_ERRORS.VALIDATION_FAILED;
	}

	return errorMessage;
}

export function getErrorMessage(errorCode: string): string {
	return (
		SIGNUP_ERROR_MAP.get(errorCode) ||
		LOGIN_ERROR_MAP.get(errorCode) ||
		SUPABASE_AUTH_ERROR_MESSAGES.UNEXPECTED_FAILURE
	);
}
