<script lang="ts">
	import { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';
	import { ContentFormat } from '$lib/api/content/ContentFormat';
	import { ContentGenerationJobWorkflowType } from '$lib/api/content-generation-jobs/ContentGenerationJobWorkflowType';
	import { useCreateContentGenerationJob } from '$lib/api/content-generation-jobs/mutations';
	import instagramLogo from '$lib/assets/instagram_logo.png';
	import linkedinLogo from '$lib/assets/linkedin_logo.png';
	import { Button } from '$lib/components/ui/button';
	import * as Empty from '$lib/components/ui/empty';
	import FileUploadZone from '$lib/components/ui/file-upload/FileUploadZone.svelte';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Calendar, ImageIcon, Megaphone, Package } from '@lucide/svelte';
	import { SvelteDate } from 'svelte/reactivity';

	type Brand = { id: string };

	type Props = {
		brand: Brand;
		onJobCreated: (jobId: string) => void;
		disabled?: boolean;
	};

	let { brand, onJobCreated, disabled = false }: Props = $props();

	const createMutation = useCreateContentGenerationJob();

	let fileInputRef = $state<HTMLInputElement | null>(null);
	let prompt = $state('');
	let scheduledAt = $state<string>(getDefaultScheduledAt());
	let selectedChannel = $state<ContentChannelName>(ContentChannelName.INSTAGRAM);
	let error = $state<string | null>(null);
	let uploadedFile = $state<File | null>(null);
	let useProductLifestyle = $state(false);

	function getDefaultScheduledAt(): string {
		const tomorrow = new SvelteDate();
		tomorrow.setDate(tomorrow.getDate() + 1);
		tomorrow.setHours(12, 0, 0, 0);
		return tomorrow.toISOString().slice(0, 16);
	}

	const workflowType = $derived.by(() => {
		if (!uploadedFile) {
			return ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_AI_GENERATED;
		}
		if (useProductLifestyle) {
			return ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE;
		}
		return ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA;
	});

	function validate(): string | null {
		if (!prompt.trim()) return 'Please enter a content prompt';
		if (!selectedChannel) return 'Please select a channel';
		const scheduledDate = new Date(scheduledAt);
		if (scheduledDate <= new Date()) return 'Scheduled date must be in the future';
		return null;
	}

	function handleSubmit() {
		const validationError = validate();
		if (validationError) {
			error = validationError;
			return;
		}
		error = null;
		const scheduledDate = new Date(scheduledAt);
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const userInput: any = {
			workflow_type: workflowType,
			prompt: prompt.trim(),
			channel: selectedChannel,
			scheduled_at: scheduledDate.toISOString()
		};
		if (workflowType === ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_FROM_USER_MEDIA) {
			userInput.image_url = '';
		}
		if (workflowType === ContentGenerationJobWorkflowType.TEXT_WITH_SINGLE_IMAGE_PRODUCT_LIFESTYLE) {
			userInput.product_image_url = '';
		}
		const request = {
			brand_id: brand.id,
			user_input: userInput,
			content_format: ContentFormat.TEXT_WITH_SINGLE_IMAGE
		};
		createMutation.mutate(
			{ request, file: uploadedFile || undefined },
			{
				onSuccess: (job) => onJobCreated(job.id),
				onError: (err) => {
					error = err instanceof Error ? err.message : 'Failed to create content generation job';
				}
			}
		);
	}

	function handleFileChange(file: File) {
		uploadedFile = file;
	}

	function handleFileRemove() {
		uploadedFile = null;
		useProductLifestyle = false;
		if (fileInputRef) fileInputRef.value = '';
	}

	function triggerFileInput() {
		if (disabled || !fileInputRef) return;
		fileInputRef.click();
	}
</script>

<input
	bind:this={fileInputRef}
	type="file"
	accept="image/*"
	{disabled}
	class="hidden"
	onchange={(e) => {
		const target = e.target as HTMLInputElement;
		if (target.files?.[0]) handleFileChange(target.files[0]);
	}}
/>

<div class="grid grid-cols-1 gap-6 min-w-0 flex-1 lg:grid-cols-[minmax(0,20rem)_minmax(0,1fr)]">
	<div class="space-y-6 min-w-0">
		<div class="space-y-2">
			<Label for="prompt">Content Description</Label>
			<Textarea
				id="prompt"
				bind:value={prompt}
				placeholder="Example: Create a post about our new product launch, highlighting its eco-friendly features and targeting environmentally conscious consumers."
				class="min-h-[120px]"
				{disabled}
			/>
		</div>

		<div class="space-y-3">
			<Label>Channel</Label>
			<div class="flex flex-col gap-3">
				<label class="flex items-center gap-3 cursor-pointer">
					<input
						type="radio"
						name="channel"
						value={ContentChannelName.INSTAGRAM}
						checked={selectedChannel === ContentChannelName.INSTAGRAM}
						onchange={() => (selectedChannel = ContentChannelName.INSTAGRAM)}
						{disabled}
						class="h-4 w-4"
					/>
					<img src={instagramLogo} alt="Instagram" class="h-5 w-5" />
					<span class="text-sm font-medium">Instagram</span>
				</label>
				<label class="flex items-center gap-3 cursor-pointer">
					<input
						type="radio"
						name="channel"
						value={ContentChannelName.LINKEDIN}
						checked={selectedChannel === ContentChannelName.LINKEDIN}
						onchange={() => (selectedChannel = ContentChannelName.LINKEDIN)}
						{disabled}
						class="h-4 w-4"
					/>
					<img src={linkedinLogo} alt="LinkedIn" class="h-5 w-5" />
					<span class="text-sm font-medium">LinkedIn</span>
				</label>
			</div>
		</div>

		<div class="space-y-2">
			<Label for="scheduled-at" class="flex items-center gap-2">
				<Calendar class="h-4 w-4" />
				Scheduled Date & Time
			</Label>
			<Input
				id="scheduled-at"
				type="datetime-local"
				bind:value={scheduledAt}
				{disabled}
				class="w-full"
			/>
			<p class="text-sm text-muted-foreground">Default: Tomorrow at 12:00 PM</p>
		</div>

		<Button onclick={handleSubmit} disabled={disabled || createMutation.isPending} class="w-full">
			{#if createMutation.isPending}
				<Megaphone class="mr-2 h-4 w-4" />
				Creating...
			{:else}
				<Megaphone class="mr-2 h-4 w-4" />
				Generate Content
			{/if}
		</Button>
	</div>

	<div class="min-w-0 overflow-y-auto flex flex-col">
		<Label class="shrink-0 mb-2">Upload Image (Optional)</Label>
		{#if uploadedFile}
			<div class="min-w-0 max-w-full space-y-4">
				<FileUploadZone
					file={uploadedFile}
					accept="image/*"
					{disabled}
					onFileChange={handleFileChange}
					onFileRemove={handleFileRemove}
				/>
				<div
					class="flex items-center justify-between gap-4 p-4 rounded-lg border bg-muted/30"
				>
					<div class="flex items-start gap-3">
						<Package class="h-5 w-5 text-muted-foreground shrink-0 mt-0.5" />
						<div class="space-y-1">
							<Label for="product-lifestyle-switch" class="text-sm font-medium cursor-pointer">
								Generate Product Lifestyle Image
							</Label>
							<p class="text-xs text-muted-foreground">
								AI will create a lifestyle scene featuring your product while preserving its exact
								appearance.
							</p>
						</div>
					</div>
					<Switch
						id="product-lifestyle-switch"
						bind:checked={useProductLifestyle}
						disabled={disabled}
					/>
				</div>
			</div>
		{:else}
			<Empty.Root class="flex-1 min-h-[200px] border border-dashed">
				<Empty.Header>
					<Empty.Media variant="icon">
						<ImageIcon />
					</Empty.Media>
					<Empty.Title>No image selected</Empty.Title>
					<Empty.Description>
						Upload your own image or leave empty to generate with AI. With an image, you can
						optionally enable "Generate Product Lifestyle Image".
					</Empty.Description>
				</Empty.Header>
				<Empty.Content>
					<Button variant="outline" size="sm" onclick={triggerFileInput} {disabled}>
						<ImageIcon class="mr-2 h-4 w-4" />
						Upload image
					</Button>
				</Empty.Content>
			</Empty.Root>
		{/if}
	</div>
</div>

{#if error}
	<div class="text-sm text-destructive bg-destructive/10 p-3 rounded-lg mt-4">
		{error}
	</div>
{/if}
