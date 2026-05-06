export enum ContentPillarFunnelStage {
	AWARENESS = 'AWARENESS',
	CONSIDERATION = 'CONSIDERATION',
	CONVERSION = 'CONVERSION',
	LOYALTY = 'LOYALTY'
}

export enum ContentPillarBusinessGoal {
	DRIVE_ENGAGEMENT = 'DRIVE_ENGAGEMENT',
	INCREASE_CONVERSION = 'INCREASE_CONVERSION',
	BUILD_TRUST = 'BUILD_TRUST',
	GENERATE_LEADS = 'GENERATE_LEADS',
	RETENTION = 'RETENTION'
}

export enum ContentPillarType {
	EDUCATION = 'EDUCATION',
	PRODUCT_SERVICE = 'PRODUCT_SERVICE',
	SOCIAL_PROOF = 'SOCIAL_PROOF',
	BEHIND_THE_SCENES = 'BEHIND_THE_SCENES',
	ENTERTAINMENT = 'ENTERTAINMENT',
	COMMUNITY = 'COMMUNITY',
	THOUGHT_LEADERSHIP = 'THOUGHT_LEADERSHIP'
}

export enum ContentType {
	TUTORIAL = 'TUTORIAL',
	TIP = 'TIP',
	GUIDE = 'GUIDE',
	FRAMEWORK = 'FRAMEWORK',
	MYTH = 'MYTH',
	MISTAKE = 'MISTAKE',
	INDUSTRY_INSIGHT = 'INDUSTRY_INSIGHT',
	DEMO = 'DEMO',
	FEATURE_HIGHLIGHT = 'FEATURE_HIGHLIGHT',
	PRODUCT_USE = 'PRODUCT_USE',
	BEFORE_AFTER = 'BEFORE_AFTER',
	BENEFIT = 'BENEFIT',
	COMPARISON = 'COMPARISON',
	TESTIMONIAL = 'TESTIMONIAL',
	REVIEW = 'REVIEW',
	CASE_STUDY = 'CASE_STUDY',
	CLIENT_STORY = 'CLIENT_STORY',
	RESULT = 'RESULT',
	SCREENSHOT = 'SCREENSHOT',
	FOUNDER_STORY = 'FOUNDER_STORY',
	TEAM_HIGHLIGHT = 'TEAM_HIGHLIGHT',
	PROCESS = 'PROCESS',
	PRODUCT_BUILDING = 'PRODUCT_BUILDING',
	DAILY_WORK = 'DAILY_WORK',
	MEME = 'MEME',
	TREND = 'TREND',
	RELATABLE_POST = 'RELATABLE_POST',
	HUMOR = 'HUMOR',
	CULTURAL_COMMENTARY = 'CULTURAL_COMMENTARY',
	OPINION = 'OPINION',
	PREDICTION = 'PREDICTION',
	HOT_TAKE = 'HOT_TAKE',
	POLL = 'POLL',
	QUESTION = 'QUESTION',
	DISCUSSION = 'DISCUSSION',
	CHALLENGE = 'CHALLENGE'
}

export interface ContentPillarResponse {
	id: string;
	name: string;
	business_goal: ContentPillarBusinessGoal;
	type: ContentPillarType;
	funnel_stage: ContentPillarFunnelStage;
	content_types: ContentType[];
	audience_ids: string[];
	hooks: string[];
	calls_to_action: string[];
}

export interface ContentPillarParsed {
	id: string;
	name: string;
	businessGoal: ContentPillarBusinessGoal;
	type: ContentPillarType;
	funnelStage: ContentPillarFunnelStage;
	contentTypes: ContentType[];
	audienceIds: string[];
	hooks: string[];
	callsToAction: string[];
}

export function contentPillarFromResponse(response: ContentPillarResponse): ContentPillarParsed {
	return {
		id: response.id,
		name: response.name,
		businessGoal: response.business_goal,
		type: response.type,
		funnelStage: response.funnel_stage,
		contentTypes: response.content_types,
		audienceIds: response.audience_ids,
		hooks: response.hooks,
		callsToAction: response.calls_to_action
	};
}

export function contentPillarToRequest(parsed: ContentPillarParsed): ContentPillarResponse {
	return {
		id: parsed.id,
		name: parsed.name,
		business_goal: parsed.businessGoal,
		type: parsed.type,
		funnel_stage: parsed.funnelStage,
		content_types: parsed.contentTypes,
		audience_ids: parsed.audienceIds,
		hooks: parsed.hooks,
		calls_to_action: parsed.callsToAction
	};
}
