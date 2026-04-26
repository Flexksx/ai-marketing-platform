export type QueryTuning = {
	staleTime?: number;
	gcTime?: number;
	retry?: number | boolean;
	refetchOnWindowFocus?: boolean;
};
