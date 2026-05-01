export type ToneDimensionKey = 'formality' | 'humour' | 'irreverence' | 'enthusiasm';

export interface ToneDimensionLevel {
	scaleNumber: number;
	name: string;
	description: string;
}

export interface ToneDimension {
	key: ToneDimensionKey;
	label: string;
	levels: ToneDimensionLevel[];
}

const FORMALITY_LEVELS: ToneDimensionLevel[] = [
	{
		scaleNumber: 1,
		name: 'Casual / Peer',
		description:
			"Use slang, contractions ('we're'), and sentence fragments. Write like a text message to a friend."
	},
	{
		scaleNumber: 2,
		name: 'Conversational',
		description:
			'Write as you speak. Use standard English but avoid jargon. Contractions are okay. Be friendly but polite.'
	},
	{
		scaleNumber: 3,
		name: 'Professional',
		description:
			'Use standard business English. Avoid contractions. Use precise terminology. Be objective.'
	},
	{
		scaleNumber: 4,
		name: 'Academic / Formal',
		description:
			'Use elevated vocabulary and complex sentence structures. Avoid all colloquialisms. Tone must be authoritative.'
	}
];

const ENTHUSIASM_LEVELS: ToneDimensionLevel[] = [
	{
		scaleNumber: 1,
		name: 'Matter-of-Fact',
		description:
			"Zero fluff. State facts only. Do not use adjectives like 'great' or 'unique'. No exclamation marks."
	},
	{
		scaleNumber: 2,
		name: 'Calm',
		description:
			"Use 'Quiet Confidence'. Focus on stability and reliability. Avoid hype words."
	},
	{
		scaleNumber: 3,
		name: 'Engaging',
		description: 'Be positive and encouraging. Use active verbs.'
	},
	{
		scaleNumber: 4,
		name: 'Hype / High Energy',
		description:
			"Use high-arousal language ('Incredible', 'Now'). Short, punchy sentences."
	}
];

const HUMOUR_LEVELS: ToneDimensionLevel[] = [
	{
		scaleNumber: 1,
		name: 'Serious',
		description:
			'STRICTLY SERIOUS: Do not use jokes, puns, or wordplay. The topic is too sensitive for humor.'
	},
	{
		scaleNumber: 2,
		name: 'Light',
		description:
			'Generally serious, but you may use a subtle metaphor or light turn of phrase to be relatable.'
	},
	{
		scaleNumber: 3,
		name: 'Witty',
		description:
			'Use clever wordplay, double entendres, or dry wit. Reward the reader for paying attention.'
	},
	{
		scaleNumber: 4,
		name: 'Humorous',
		description:
			'Be entertaining first. Jokes, memes, and playful exaggeration are encouraged. Don\'t be boring.'
	}
];

const IRREVERENCE_LEVELS: ToneDimensionLevel[] = [
	{
		scaleNumber: 1,
		name: 'Respectful',
		description:
			'Be deferential and polite. Treat the user and competitors with high respect. Never be snarky.'
	},
	{
		scaleNumber: 2,
		name: 'Direct',
		description:
			'Be confident but polite. Call a spade a spade, but avoid confrontation.'
	},
	{
		scaleNumber: 3,
		name: 'Cheeky',
		description:
			'You can be slightly provocative. Poke fun at industry clichés. Be a bit rebellious.'
	},
	{
		scaleNumber: 4,
		name: 'Provocative',
		description:
			'Be bold and rebellious. Challenge the status quo aggressively. Sarcasm and sharp critiques are allowed.'
	}
];

export const TONE_DIMENSION_DATA: Record<ToneDimensionKey, ToneDimension> = {
	formality: { key: 'formality', label: 'Formality', levels: FORMALITY_LEVELS },
	enthusiasm: { key: 'enthusiasm', label: 'Enthusiasm', levels: ENTHUSIASM_LEVELS },
	humour: { key: 'humour', label: 'Humour', levels: HUMOUR_LEVELS },
	irreverence: { key: 'irreverence', label: 'Irreverence', levels: IRREVERENCE_LEVELS }
};

export function getLevelDescription(
	dimensionKey: ToneDimensionKey,
	scaleNumber: number
): ToneDimensionLevel | undefined {
	const dimension = TONE_DIMENSION_DATA[dimensionKey];
	return dimension.levels.find((l) => l.scaleNumber === scaleNumber);
}
