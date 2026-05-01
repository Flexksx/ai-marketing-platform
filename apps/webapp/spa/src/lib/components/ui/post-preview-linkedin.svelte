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

<div class="w-full max-w-2xl bg-white rounded-lg border border-gray-300 shadow-sm overflow-hidden">
	<div class="p-4 border-b border-gray-200 flex items-start gap-3">
		<div class="h-12 w-12 rounded-full bg-[#0077b5] flex items-center justify-center flex-shrink-0">
			<div class="h-10 w-10 rounded-full bg-white flex items-center justify-center">
				<div class="h-8 w-8 rounded-full bg-gray-300"></div>
			</div>
		</div>
		<div class="flex-1 min-w-0">
			<div class="h-4 w-32 bg-gray-300 rounded mb-1"></div>
			<div class="h-3 w-24 bg-gray-200 rounded mb-2"></div>
			<div class="h-3 w-20 bg-gray-200 rounded"></div>
		</div>
		<div class="h-5 w-5 text-gray-600">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"
				class="w-full h-full"
			>
				<circle cx="12" cy="12" r="1" />
				<circle cx="19" cy="12" r="1" />
				<circle cx="5" cy="12" r="1" />
			</svg>
		</div>
	</div>

	{#if post.caption}
		<div class="p-4 pb-3">
			<p class="text-gray-900 text-sm leading-relaxed whitespace-pre-wrap break-words">{post.caption}</p>
		</div>
	{/if}

	{#if post.image_url}
		<div class="bg-gray-100">
			<img
				src={post.image_url}
				alt={post.caption || 'Post image'}
				class="w-full max-h-[500px] object-contain"
			/>
		</div>
	{:else}
		<div class="h-64 bg-gray-100 flex items-center justify-center">
			<p class="text-gray-400 text-sm">No image</p>
		</div>
	{/if}

	<div class="p-4 border-t border-gray-200">
		<div class="flex items-center justify-between text-gray-600 text-sm mb-3">
			<div class="flex items-center gap-1">
				<div class="h-5 w-5 rounded-full bg-[#0077b5] flex items-center justify-center">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="white"
						class="h-3 w-3"
					>
						<path
							d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
						/>
					</svg>
				</div>
				<span>123</span>
			</div>
			<div class="text-gray-500">12 comments</div>
		</div>

		<div class="flex items-center justify-around border-t border-gray-200 pt-2">
			<button
				type="button"
				class="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-50 rounded transition-colors"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="h-5 w-5"
				>
					<path
						d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z"
					/>
				</svg>
				<span class="text-sm font-medium">Like</span>
			</button>
			<button
				type="button"
				class="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-50 rounded transition-colors"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="h-5 w-5"
				>
					<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
				</svg>
				<span class="text-sm font-medium">Comment</span>
			</button>
			<button
				type="button"
				class="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-50 rounded transition-colors"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="h-5 w-5"
				>
					<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
					<polyline points="16 6 12 2 8 6" />
					<line x1="12" y1="2" x2="12" y2="15" />
				</svg>
				<span class="text-sm font-medium">Share</span>
			</button>
			<button
				type="button"
				class="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-50 rounded transition-colors"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					class="h-5 w-5"
				>
					<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
				</svg>
				<span class="text-sm font-medium">Send</span>
			</button>
		</div>
	</div>
</div>

