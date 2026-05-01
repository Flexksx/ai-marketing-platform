<script lang="ts">
	interface Props {
		text: string;
	}

	let { text }: Props = $props();
</script>

<span
	class="inline-flex max-w-full items-center rounded-full bg-muted px-2 py-0.5 text-[10px] leading-tight text-muted-foreground"
>
	<span class="truncate">{text}</span>
</span>

