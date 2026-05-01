<script lang="ts">
	import { Spring } from 'svelte/motion';

	let { imageUrl, index }: { imageUrl: string; index: number } = $props();

	const initialX = typeof window !== 'undefined' ? Math.random() * window.innerWidth : 0;
	const initialY = typeof window !== 'undefined' ? Math.random() * window.innerHeight : 0;
	const initialRotation = Math.random() * 360;
	const scale = 0.3 + Math.random() * 0.4;
	const speed = 2000 + Math.random() * 1000;

	const xSpring = new Spring(initialX, { stiffness: 0.05, damping: 0.3 });
	const ySpring = new Spring(initialY, { stiffness: 0.05, damping: 0.3 });
	const rotationSpring = new Spring(initialRotation, { stiffness: 0.03, damping: 0.2 });

	let x = $state(xSpring.current);
	let y = $state(ySpring.current);
	let rotation = $state(rotationSpring.current);

	$effect(() => {
		if (typeof window === 'undefined') return;

		// Create floating animation
		const animate = () => {
			const time = Date.now() / speed;
			const newX = initialX + Math.sin(time + index) * 80;
			const newY = initialY + Math.cos(time + index) * 80;
			const newRotation = initialRotation + Math.sin(time * 0.5 + index) * 10;

			xSpring.set(newX);
			ySpring.set(newY);
			rotationSpring.set(newRotation);

			// Update reactive state
			x = xSpring.current;
			y = ySpring.current;
			rotation = rotationSpring.current;
		};

		const interval = setInterval(animate, 50);
		return () => clearInterval(interval);
	});
</script>

<div
	class="absolute pointer-events-none z-0 opacity-30 hover:opacity-50 transition-opacity duration-300"
	style="left: {x}px; top: {y}px; transform: rotate({rotation}deg) scale({scale});"
>
	<img
		src={imageUrl}
		alt="Brand image"
		class="w-32 h-32 object-cover rounded-lg shadow-lg"
		loading="lazy"
	/>
</div>

