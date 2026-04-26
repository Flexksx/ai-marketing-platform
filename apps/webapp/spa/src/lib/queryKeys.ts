const defaultBrandsSearchParams: Record<string, unknown> = {};

export const queryKeys = {
	auth: {
		root: () => ["auth"] as const,
		session: () => ["auth", "session"] as const,
	},
	brands: (searchParams: Record<string, unknown> = defaultBrandsSearchParams) =>
		["brands", searchParams] as const,
	brand: (id: string) => ["brand", id] as const,
	brandContents: (searchParams: { brandId: string }) =>
		["brand-contents", searchParams.brandId] as const,
	brandContent: (contentItemId: string) =>
		["brand-content", contentItemId] as const,
};
