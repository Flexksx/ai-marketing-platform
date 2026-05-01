export interface BrandSearchRequest {
	user_id: string;
	name?: string | null;
	limit?: number | null;
	offset?: number | null;
}
