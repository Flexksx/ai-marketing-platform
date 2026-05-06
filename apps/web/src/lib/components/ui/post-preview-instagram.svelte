<script lang="ts">
	type Props = {
		post: {
			id: string;
			caption: string | null;
			image_url: string | null;
			channels: string[];
		};
	};
	let { post }: Props = $props();
</script>

<div class="w-full max-w-md bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
	<div class="p-3 border-b border-gray-200 flex items-center gap-3">
		<div class="h-8 w-8 rounded-full bg-gradient-to-br from-purple-500 via-pink-500 to-orange-500 flex items-center justify-center">
			<div class="h-7 w-7 rounded-full bg-white flex items-center justify-center">
				<div class="h-6 w-6 rounded-full bg-gray-300"></div>
			</div>
		</div>
		<div class="flex-1">
			<div class="h-4 w-24 bg-gray-300 rounded mb-1"></div>
			<div class="h-3 w-16 bg-gray-200 rounded"></div>
		</div>
		<div class="h-6 w-6">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="currentColor"
				class="w-full h-full text-gray-700"
			>
				<path
					d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"
				/>
			</svg>
		</div>
	</div>

	{#if post.image_url}
		<div class="aspect-square bg-gray-100 flex items-center justify-center">
			<img
				src={post.image_url}
				alt={post.caption || 'Post image'}
				class="w-full h-full object-cover"
			/>
		</div>
	{:else}
		<div class="aspect-square bg-gray-100 flex items-center justify-center">
			<p class="text-gray-400 text-sm">No image</p>
		</div>
	{/if}

	<div class="p-3 space-y-2">
		<div class="flex items-center gap-4">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="h-6 w-6 text-gray-900"
			>
				<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z" />
			</svg>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="h-6 w-6 text-gray-900"
			>
				<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
			</svg>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="h-6 w-6 text-gray-900"
			>
				<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
				<polyline points="16 6 12 2 8 6" />
				<line x1="12" y1="2" x2="12" y2="15" />
			</svg>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="h-6 w-6 text-gray-900 ml-auto"
			>
				<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
			</svg>
		</div>

		<div class="text-sm font-semibold text-gray-900 mb-1">likes</div>

		{#if post.caption}
			<div class="text-sm text-gray-900 break-words">
				<span class="font-semibold">username</span>
				<span class="ml-1 whitespace-pre-wrap break-words">{post.caption}</span>
			</div>
		{:else}
			<div class="text-sm text-gray-500">No caption</div>
		{/if}

		<div class="text-xs text-gray-500 uppercase tracking-wide mt-2">2 hours ago</div>
	</div>
</div>

