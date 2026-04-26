export const authQueryKeys = {
	root: () => ["auth"] as const,
	session: () => [...authQueryKeys.root(), "session"] as const,
} as const;
