import { writable, get } from 'svelte/store';

export const campaignSuggestionJobIds = writable<Record<string, string[]>>({});

export const addJobIds = (brandId: string, jobIds: string[]) => {
	campaignSuggestionJobIds.update((state) => {
		const existing = state[brandId] || [];
		const newIds = jobIds.filter((id) => !existing.includes(id));
		return {
			...state,
			[brandId]: [...existing, ...newIds]
		};
	});
};

export const removeJobId = (brandId: string, jobId: string) => {
	campaignSuggestionJobIds.update((state) => {
		const existing = state[brandId] || [];
		return {
			...state,
			[brandId]: existing.filter((id) => id !== jobId)
		};
	});
};

export const getJobIds = (brandId: string): string[] => {
	const state = get(campaignSuggestionJobIds);
	return state[brandId] || [];
};

export const clearJobIds = (brandId: string) => {
	campaignSuggestionJobIds.update((state) => {
		const newState = { ...state };
		delete newState[brandId];
		return newState;
	});
};

