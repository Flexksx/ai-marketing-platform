import { BrandAudienceAgeRange } from '$lib/api/generated/models/BrandAudienceAgeRange';
import { BrandAudienceGender } from '$lib/api/generated/models/BrandAudienceGender';
import { BrandAudienceIncomeRange } from '$lib/api/generated/models/BrandAudienceIncomeRange';
import type { ContentChannelName } from '$lib/api/generated/models/ContentChannelName';
import {
	Baby,
	BadgeDollarSign,
	Banknote,
	CircleUserRound,
	Instagram,
	LandPlot,
	LineChart,
	Linkedin,
	Wallet,
	Waypoints,
	Wheat,
	Workflow
} from 'lucide-svelte';

type LabeledOption<T extends string, IconType> = {
	value: T;
	shortLabel: string;
	fullLabel: string;
	icon: IconType;
};

type AgeRangeOption = LabeledOption<BrandAudienceAgeRange, typeof Baby>;
type GenderOption = LabeledOption<BrandAudienceGender, typeof CircleUserRound>;
type IncomeRangeOption = LabeledOption<BrandAudienceIncomeRange, typeof Wallet>;

type ChannelOption = {
	value: ContentChannelName;
	shortLabel: string;
	fullLabel: string;
	icon: typeof Instagram;
};

export const AGE_RANGE_OPTIONS: AgeRangeOption[] = [
	{
		value: BrandAudienceAgeRange.teens,
		shortLabel: 'Teens',
		fullLabel: 'Teens (13–19)',
		icon: Baby
	},
	{
		value: BrandAudienceAgeRange.youngAdults,
		shortLabel: 'Young',
		fullLabel: 'Young adults (20–29)',
		icon: Waypoints
	},
	{
		value: BrandAudienceAgeRange.adults,
		shortLabel: 'Adults',
		fullLabel: 'Adults (30–39)',
		icon: Workflow
	},
	{
		value: BrandAudienceAgeRange.middleAged,
		shortLabel: 'Middle',
		fullLabel: 'Middle aged (40–59)',
		icon: LineChart
	},
	{
		value: BrandAudienceAgeRange.seniors,
		shortLabel: 'Seniors',
		fullLabel: 'Seniors (60+)',
		icon: Wheat
	},
	{
		value: BrandAudienceAgeRange.any,
		shortLabel: 'Any',
		fullLabel: 'Any age',
		icon: Waypoints
	}
];

export const GENDER_OPTIONS: GenderOption[] = [
	{
		value: BrandAudienceGender.male,
		shortLabel: 'Male',
		fullLabel: 'Male',
		icon: CircleUserRound
	},
	{
		value: BrandAudienceGender.female,
		shortLabel: 'Female',
		fullLabel: 'Female',
		icon: CircleUserRound
	},
	{
		value: BrandAudienceGender.any,
		shortLabel: 'Any',
		fullLabel: 'Any gender',
		icon: CircleUserRound
	}
];

export const INCOME_RANGE_OPTIONS: IncomeRangeOption[] = [
	{
		value: BrandAudienceIncomeRange.lowIncome,
		shortLabel: 'Low',
		fullLabel: 'Low income',
		icon: LandPlot
	},
	{
		value: BrandAudienceIncomeRange.middleIncome,
		shortLabel: 'Middle',
		fullLabel: 'Middle income',
		icon: Wallet
	},
	{
		value: BrandAudienceIncomeRange.upperMiddleIncome,
		shortLabel: 'Upper',
		fullLabel: 'Upper middle income',
		icon: Banknote
	},
	{
		value: BrandAudienceIncomeRange.highIncome,
		shortLabel: 'High',
		fullLabel: 'High income',
		icon: BadgeDollarSign
	},
	{
		value: BrandAudienceIncomeRange.any,
		shortLabel: 'Any',
		fullLabel: 'Any income',
		icon: Wallet
	}
];

export const CHANNEL_OPTIONS: ChannelOption[] = [
	{
		value: 'INSTAGRAM',
		shortLabel: 'IG',
		fullLabel: 'Instagram',
		icon: Instagram
	},
	{
		value: 'LINKEDIN',
		shortLabel: 'LI',
		fullLabel: 'LinkedIn',
		icon: Linkedin
	}
];

export function getAgeRangeLabels(value: BrandAudienceAgeRange) {
	const option = AGE_RANGE_OPTIONS.find((item) => item.value === value);
	return option ?? AGE_RANGE_OPTIONS.find((item) => item.value === 'ANY')!;
}

export function getGenderLabels(value: BrandAudienceGender) {
	const option = GENDER_OPTIONS.find((item) => item.value === value);
	return option ?? GENDER_OPTIONS.find((item) => item.value === 'ANY')!;
}

export function getIncomeRangeLabels(value: BrandAudienceIncomeRange) {
	const option = INCOME_RANGE_OPTIONS.find((item) => item.value === value);
	return option ?? INCOME_RANGE_OPTIONS.find((item) => item.value === 'ANY')!;
}

export function getChannelOption(value: ContentChannelName) {
	return CHANNEL_OPTIONS.find((item) => item.value === value) ?? CHANNEL_OPTIONS[0];
}
