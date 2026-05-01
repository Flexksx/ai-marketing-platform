export function getColor(color: string, fallback: string): string {
	if (!color || color.trim() === '') return fallback;
	return color.startsWith('#') ? color : `#${color}`;
}

export function getToneOfVoiceColor(level: number): string {
	if (level === 1) return '#3b82f6';
	if (level === 2) return '#22c55e';
	if (level === 3) return '#eab308';
	if (level === 4) return '#f97316';
	return '#6b7280';
}

export function getChannelLevelColor(level: number): string {
	if (level === 0) return 'bg-slate-400';
	if (level === 1) return 'bg-blue-500';
	if (level === 2) return 'bg-green-500';
	if (level === 3) return 'bg-yellow-500';
	if (level === 4) return 'bg-orange-500';
	if (level === 5) return 'bg-red-500';
	return 'bg-muted';
}
