<script lang="ts">
	type Props = {
		date: Date;
		currentDate: Date;
	};

	let { date, currentDate }: Props = $props();

	const isToday = $derived(
		date.getDate() === currentDate.getDate() &&
			date.getMonth() === currentDate.getMonth() &&
			date.getFullYear() === currentDate.getFullYear()
	);

	const dayName = $derived(date.toLocaleDateString('en-US', { weekday: 'short' }));
	const monthShort = $derived(date.toLocaleDateString('en-US', { month: 'short' }));
</script>

<div
	class="text-lg font-semibold {isToday
		? 'bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center mx-auto'
		: ''}"
>
	{date.getDate()}
</div>
<div class="text-muted-foreground text-xs">{dayName}</div>
<div class="text-muted-foreground text-xs">{monthShort}</div>
