import {
	BrandAudienceAgeRange,
	BrandAudienceGender,
	BrandAudienceIncomeRange
} from '$lib/api/brand-data/model/BrandData';
import type { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';
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
		value: BrandAudienceAgeRange.TEENS,
		shortLabel: 'Teens',
		fullLabel: 'Teens (13–19)',
		icon: Baby
	},
	{
		value: BrandAudienceAgeRange.YOUNG_ADULTS,
		shortLabel: 'Young',
		fullLabel: 'Young adults (20–29)',
		icon: Waypoints
	},
	{
		value: BrandAudienceAgeRange.ADULTS,
		shortLabel: 'Adults',
		fullLabel: 'Adults (30–39)',
		icon: Workflow
	},
	{
		value: BrandAudienceAgeRange.MIDDLE_AGED,
		shortLabel: 'Middle',
		fullLabel: 'Middle aged (40–59)',
		icon: LineChart
	},
	{
		value: BrandAudienceAgeRange.SENIORS,
		shortLabel: 'Seniors',
		fullLabel: 'Seniors (60+)',
		icon: Wheat
	},
	{
		value: BrandAudienceAgeRange.ANY,
		shortLabel: 'Any',
		fullLabel: 'Any age',
		icon: Waypoints
	}
];

export const GENDER_OPTIONS: GenderOption[] = [
	{
		value: BrandAudienceGender.MALE,
		shortLabel: 'Male',
		fullLabel: 'Male',
		icon: CircleUserRound
	},
	{
		value: BrandAudienceGender.FEMALE,
		shortLabel: 'Female',
		fullLabel: 'Female',
		icon: CircleUserRound
	},
	{
		value: BrandAudienceGender.ANY,
		shortLabel: 'Any',
		fullLabel: 'Any gender',
		icon: CircleUserRound
	}
];

export const INCOME_RANGE_OPTIONS: IncomeRangeOption[] = [
	{
		value: BrandAudienceIncomeRange.LOW_INCOME,
		shortLabel: 'Low',
		fullLabel: 'Low income',
		icon: LandPlot
	},
	{
		value: BrandAudienceIncomeRange.MIDDLE_INCOME,
		shortLabel: 'Middle',
		fullLabel: 'Middle income',
		icon: Wallet
	},
	{
		value: BrandAudienceIncomeRange.UPPER_MIDDLE_INCOME,
		shortLabel: 'Upper',
		fullLabel: 'Upper middle income',
		icon: Banknote
	},
	{
		value: BrandAudienceIncomeRange.HIGH_INCOME,
		shortLabel: 'High',
		fullLabel: 'High income',
		icon: BadgeDollarSign
	},
	{
		value: BrandAudienceIncomeRange.ANY,
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
