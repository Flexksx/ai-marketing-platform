import type { BrandArchetypeName } from '$lib/api/generated/models/BrandArchetypeName';

export const ARCHETYPE_LABELS: Record<BrandArchetypeName, string> = {
	INNOCENT: 'Innocent',
	EVERYMAN: 'Everyman',
	HERO: 'Hero',
	OUTLAW: 'Outlaw',
	EXPLORER: 'Explorer',
	CREATOR: 'Creator',
	RULER: 'Ruler',
	MAGICIAN: 'Magician',
	LOVER: 'Lover',
	CAREGIVER: 'Caregiver',
	JESTER: 'Jester',
	SAGE: 'Sage'
};

export const ARCHETYPE_DESCRIPTIONS: Record<BrandArchetypeName, string> = {
	INNOCENT:
		'Your brand is a beacon of simplicity and trust — it promises peace of mind and a return to what feels pure, ethical, and uncomplicated.',
	EVERYMAN:
		'Your brand is a reliable neighbor — down-to-earth, inclusive, and built for real life, delivering honest value without pretense or elitism.',
	HERO: 'Your brand is a force for achievement — it inspires people to push past limits, proving that courage, discipline, and excellence lead to extraordinary results.',
	OUTLAW:
		'Your brand is a badge of rebellion — it challenges the status quo, celebrates non-conformity, and turns tension with the mainstream into a source of pride.',
	EXPLORER:
		'Your brand is an invitation to discover — it celebrates autonomy, curiosity, and the freedom to find yourself beyond the familiar.',
	CREATOR:
		'Your brand is an engine of imagination — it empowers people to build, design, and ship their vision by providing the tools and inspiration to make ideas real.',
	RULER:
		'Your brand is the gold standard — it projects authority, competence, and world-class quality, setting the benchmark that others aspire to reach.',
	MAGICIAN:
		'Your brand is a catalyst for transformation — it turns the seemingly impossible into effortless reality through insight, innovation, and a touch of wonder.',
	LOVER:
		'Your brand is a celebration of connection — it elevates the senses, deepens relationships, and invites people to savor beauty, intimacy, and the art of living well.',
	CAREGIVER:
		'Your brand is a pillar of empathy — it centers service and protection, reducing anxiety and building community by genuinely putting people first.',
	JESTER:
		'Your brand is a spark of joy — it entertains, disarms, and creates memorable moments by using humor to humanize and build a community around shared laughter.',
	SAGE: 'Your brand is a trusted guide to understanding — it synthesizes complex ideas into clear frameworks so people can make confident, well-informed decisions.'
};

export const BRAND_ARCHETYPE_NAMES: BrandArchetypeName[] = [
	'INNOCENT',
	'EVERYMAN',
	'HERO',
	'OUTLAW',
	'EXPLORER',
	'CREATOR',
	'RULER',
	'MAGICIAN',
	'LOVER',
	'CAREGIVER',
	'JESTER',
	'SAGE'
];

export function getArchetypeLabel(name: BrandArchetypeName): string {
	return ARCHETYPE_LABELS[name];
}

export function getArchetypeDescription(name: BrandArchetypeName): string {
	return ARCHETYPE_DESCRIPTIONS[name];
}
