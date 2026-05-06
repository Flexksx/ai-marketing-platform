export enum SentenceLengthPreference {
	SHORT = 'SHORT',
	MEDIUM = 'MEDIUM',
	LONG = 'LONG'
}

export interface BrandToneOfVoice {
	formality_level: number;
	humour_level: number;
	irreverence_level: number;
	enthusiasm_level: number;
	industry_jargon_usage_level: number;
	sentence_length_preference: SentenceLengthPreference;
	sensory_keywords: string[];
	excluded_words: string[];
	signature_words: string[];
}
