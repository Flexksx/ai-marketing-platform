import type { BrandResponse } from '../brands/brand.types';

export interface PostResponse {
	id: string;
	campaign_id: string;
	channel: 'INSTAGRAM' | 'LINKEDIN';
	caption: string;
	media_url: string;
	media_description: string | null;
	media_user_adjustments: string | null;
	scheduled_at: string | null;
	created_at: string;
	updated_at: string;
}

export interface BrandStatsResponse {
	brand: BrandResponse;
	active_campaigns_count: number;
	total_posts_count: number;
	instagram_posts_count: number;
	linkedin_posts_count: number;
	next_post: PostResponse | null;
}

export type BrandStatsListRequest = {
	limit?: number;
	offset?: number;
};
