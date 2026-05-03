export type ToneDimensionKey = 'jargon_density' | 'visual_density';

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

const JARGON_DENSITY_LEVELS: ToneDimensionLevel[] = [
	{
		scaleNumber: 1,
		name: 'Plain',
		description: 'No technical terms. Use everyday language accessible to anyone.'
	},
	{
		scaleNumber: 2,
		name: 'Light',
		description: 'A few industry terms where helpful, always explained in context.'
	},
	{
		scaleNumber: 3,
		name: 'Industry',
		description: 'Standard industry terminology assumed. No hand-holding.'
	},
	{
		scaleNumber: 4,
		name: 'Expert',
		description: 'Dense technical language. Assumes deep domain expertise.'
	}
];

const VISUAL_DENSITY_LEVELS: ToneDimensionLevel[] = [
	{
		scaleNumber: 1,
		name: 'Minimal',
		description: 'Sparse copy. Lots of whitespace. Single bold idea per unit.'
	},
	{
		scaleNumber: 2,
		name: 'Light',
		description: 'Short paragraphs, bullet points welcome. Easy to scan.'
	},
	{
		scaleNumber: 3,
		name: 'Moderate',
		description: 'Balanced text and structure. Multiple points per section.'
	},
	{
		scaleNumber: 4,
		name: 'Dense',
		description: 'Information-rich. Long-form content packed with detail.'
	}
];

export const TONE_DIMENSION_DATA: Record<ToneDimensionKey, ToneDimension> = {
	jargon_density: { key: 'jargon_density', label: 'Jargon Density', levels: JARGON_DENSITY_LEVELS },
	visual_density: { key: 'visual_density', label: 'Visual Density', levels: VISUAL_DENSITY_LEVELS }
};

export function getLevelDescription(
	dimensionKey: ToneDimensionKey,
	scaleNumber: number
): ToneDimensionLevel | undefined {
	const dimension = TONE_DIMENSION_DATA[dimensionKey];
	return dimension.levels.find((l) => l.scaleNumber === scaleNumber);
}
