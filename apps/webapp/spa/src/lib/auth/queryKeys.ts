export const queryKeys = {
	auth: () => ["auth"] as const,
	authSession: () => ["auth", "session"] as const,
} as const;
