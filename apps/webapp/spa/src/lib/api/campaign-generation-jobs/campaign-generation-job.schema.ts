export interface CampaignGenerationJobAcceptRequest {
	posting_plan_modifications?: PostingPlanItemModification[];
}

export interface PostingPlanItemModification {
	item_id: string;
	caption?: string | null;
	image_url?: string | null;
	scheduled_at?: string | null;
}
