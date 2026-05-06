<script lang="ts">
	type Props = {
		date: Date;
		currentDate: Date;
		isInView?: boolean;
	};

	let { date, currentDate, isInView = true }: Props = $props();

	const isToday = $derived(
		date.getDate() === currentDate.getDate() &&
			date.getMonth() === currentDate.getMonth() &&
			date.getFullYear() === currentDate.getFullYear()
	);
</script>

<span
	class="text-sm font-semibold {isToday
		? 'bg-primary text-primary-foreground rounded-full w-7 h-7 flex items-center justify-center'
		: isInView
			? 'text-foreground'
			: 'text-muted-foreground'}"
>
	{date.getDate()}
</span>
