<script lang="ts">
	import { resolve } from '$app/paths';
	import { CampaignGenerationJobWorkflowType } from '$lib/api/campaign-generation-jobs/CampaignGenerationJobWorkflowType';
	import { useCreateCampaignGenerationJob } from '$lib/api/campaign-generation-jobs/queries';
	import { ContentChannelName } from '$lib/api/content-channel/ContentChannelName';
	import instagramLogo from '$lib/assets/instagram_logo.png';
	import linkedinLogo from '$lib/assets/linkedin_logo.png';
	import { Button } from '$lib/components/ui/button';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Popover from '$lib/components/ui/popover';
	import { RangeCalendar } from '$lib/components/ui/range-calendar';
	import { Switch } from '$lib/components/ui/switch';
	import { Textarea } from '$lib/components/ui/textarea';
	import { navigate } from '$lib/navigation';
	import { DateFormatter, getLocalTimeZone, today } from '@internationalized/date';
	import { Calendar, ChevronDown, ImageIcon, Loader2, Package, Sparkles, X } from '@lucide/svelte';

	type Brand = {
		id: string;
	};

	type Props = {
		brand: Brand;
		open?: boolean;
	};

	let { brand, open = $bindable(false) }: Props = $props();

	const createMutation = useCreateCampaignGenerationJob();

	const rangeFormatter = new DateFormatter('en-US', {
		month: 'short',
		day: 'numeric',
		year: 'numeric'
	});

	const startDefault = today(getLocalTimeZone());
	const endDefault = startDefault.add({ days: 14 });

	let prompt = $state('');
	let campaignRange = $state({ start: startDefault, end: endDefault });
	let durationPopoverOpen = $state(false);
	let selectedChannels = $state<ContentChannelName[]>([
		ContentChannelName.INSTAGRAM,
		ContentChannelName.LINKEDIN
	]);
	let error = $state<string | null>(null);
	let uploadedFiles = $state<File[]>([]);
	let fileInputRef = $state<HTMLInputElement | null>(null);
	let useProductLifestyle = $state(false);

	const workflowType = $derived.by(() => {
		if (uploadedFiles.length === 0) {
			return CampaignGenerationJobWorkflowType.AI_GENERATED;
		}
		if (useProductLifestyle) {
			return CampaignGenerationJobWorkflowType.PRODUCT_LIFESTYLE;
		}
		return CampaignGenerationJobWorkflowType.USER_MEDIA_ONLY;
	});

	const toggleChannel = (channel: ContentChannelName) => {
		if (selectedChannels.includes(channel)) {
			selectedChannels = selectedChannels.filter((c) => c !== channel);
		} else {
			selectedChannels = [...selectedChannels, channel];
		}
	};

	const handleFileChange = (event: Event) => {
		const target = event.target as HTMLInputElement;
		if (target.files) {
			const newFiles = Array.from(target.files);
			uploadedFiles = [...uploadedFiles, ...newFiles];
			target.value = '';
		}
	};

	const removeFile = (index: number) => {
		uploadedFiles = uploadedFiles.filter((_, i) => i !== index);
		if (uploadedFiles.length === 0) {
			useProductLifestyle = false;
		}
	};

	const handleSubmit = () => {
		if (!prompt.trim()) {
			error = 'Please enter a campaign description';
			return;
		}

		if (selectedChannels.length === 0) {
			error = 'Please select at least one channel';
			return;
		}

		if (!campaignRange.end) {
			error = 'Please select the end date for the campaign';
			return;
		}

		error = null;

		createMutation.mutate(
			{
				request: {
					brand_id: brand.id,
					prompt: prompt.trim(),
					start_date: campaignRange.start.toString(),
					end_date: campaignRange.end.toString(),
					channels: selectedChannels,
					workflow_type: workflowType
				},
				files: uploadedFiles
			},
			{
				onSuccess: (job) => {
					navigate(resolve(`/brands/${brand.id}/campaigns/creation/${job.id}`));
				},
				onError: (err) => {
					error = err instanceof Error ? err.message : 'Failed to create campaign';
				}
			}
		);
	};

	const handleClose = () => {
		if (!createMutation.isPending) {
			open = false;
			prompt = '';
			campaignRange = {
				start: today(getLocalTimeZone()),
				end: today(getLocalTimeZone()).add({ days: 14 })
			};
			selectedChannels = [ContentChannelName.INSTAGRAM, ContentChannelName.LINKEDIN];
			uploadedFiles = [];
			useProductLifestyle = false;
			error = null;
		}
	};

	const durationLabel = $derived.by(() => {
		const start = campaignRange.start;
		const end = campaignRange.end;
		if (!start) return 'Select dates';
		const startStr = rangeFormatter.format(start.toDate(getLocalTimeZone()));
		if (!end) return `${startStr} – …`;
		return `${startStr} – ${rangeFormatter.format(end.toDate(getLocalTimeZone()))}`;
	});
</script>

<Dialog.Root bind:open>
	<Dialog.Content class="max-w-2xl">
		<Dialog.Header>
			<Dialog.Title class="flex items-center gap-2">
				<Sparkles class="h-5 w-5 text-purple-600" />
				Create New Content Plan
			</Dialog.Title>
			<Dialog.Description>
				Describe your content plan idea, select the duration and channels, and let AI generate
				engaging posts.
			</Dialog.Description>
		</Dialog.Header>

		<div class="space-y-6 py-4">
			<div class="space-y-2">
				<Label for="prompt">Content Plan Description</Label>
				<Textarea
					id="prompt"
					bind:value={prompt}
					placeholder="Example: Launch our new eco-friendly product line targeting millennials who care about sustainability. Focus on highlighting product benefits and our commitment to the environment."
					class="min-h-[120px]"
					disabled={createMutation.isPending}
				/>
			</div>

			<div class="space-y-2">
				<Label class="flex items-center gap-2">
					<Calendar class="h-4 w-4" />
					Content Plan Duration
				</Label>
				<Popover.Root bind:open={durationPopoverOpen}>
					<Popover.Trigger
						class="w-full [&:has(button)]:w-full"
						disabled={createMutation.isPending}
					>
						{#snippet child({ props })}
							<Button
								{...props}
								variant="outline"
								class="w-full justify-between font-normal"
								disabled={createMutation.isPending}
							>
								<span class="flex items-center gap-2">
									<Calendar class="h-4 w-4" />
									{durationLabel}
								</span>
								<ChevronDown class="h-4 w-4 opacity-50" />
							</Button>
						{/snippet}
					</Popover.Trigger>
					<Popover.Content class="w-auto p-0" align="start">
						<RangeCalendar bind:value={campaignRange} class="rounded-md border" />
					</Popover.Content>
				</Popover.Root>
				<p class="text-sm text-muted-foreground">Default: 2-week campaign from today</p>
			</div>

			<div class="space-y-3">
				<Label>Channels</Label>
				<div class="flex flex-col gap-3">
					<label class="flex items-center gap-3 cursor-pointer">
						<Checkbox
							checked={selectedChannels.includes(ContentChannelName.INSTAGRAM)}
							onCheckedChange={() => toggleChannel(ContentChannelName.INSTAGRAM)}
							disabled={createMutation.isPending}
						/>
						<img src={instagramLogo} alt="Instagram" class="h-5 w-5" />
						<span class="text-sm font-medium">Instagram</span>
					</label>
					<label class="flex items-center gap-3 cursor-pointer">
						<Checkbox
							checked={selectedChannels.includes(ContentChannelName.LINKEDIN)}
							onCheckedChange={() => toggleChannel(ContentChannelName.LINKEDIN)}
							disabled={createMutation.isPending}
						/>
						<img src={linkedinLogo} alt="LinkedIn" class="h-5 w-5" />
						<span class="text-sm font-medium">LinkedIn</span>
					</label>
				</div>
				<p class="text-sm text-muted-foreground">Select at least one channel for your campaign</p>
			</div>

			<div class="space-y-3">
				<Label class="flex items-center gap-2">
					<ImageIcon class="h-4 w-4" />
					Upload Images (Optional)
				</Label>
				<div class="space-y-3">
					<Input
						bind:ref={fileInputRef}
						type="file"
						accept="image/*"
						multiple
						onchange={handleFileChange}
						disabled={createMutation.isPending}
						class="cursor-pointer"
					/>
					{#if uploadedFiles.length > 0}
						<div class="space-y-3">
							<div class="flex items-center justify-between">
								<p class="text-sm font-medium">
									{uploadedFiles.length}
									{uploadedFiles.length === 1 ? 'image' : 'images'} selected
								</p>
								<span class="text-xs px-2 py-1 bg-primary/10 text-primary rounded-md font-medium">
									{useProductLifestyle ? 'Product Lifestyle' : 'User Media'} Workflow
								</span>
							</div>
							<div class="grid grid-cols-4 gap-2 max-h-32 overflow-y-auto p-2 border rounded-lg">
								{#each uploadedFiles as file, index (file.name + index)}
									<div class="relative group aspect-square">
										<img
											src={URL.createObjectURL(file)}
											alt={file.name}
											class="w-full h-full object-cover rounded border"
										/>
										<button
											type="button"
											onclick={() => removeFile(index)}
											disabled={createMutation.isPending}
											class="absolute -top-1 -right-1 bg-destructive text-destructive-foreground rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-50"
											aria-label="Remove image"
										>
											<X class="h-3 w-3" />
										</button>
									</div>
								{/each}
							</div>
							<div
								class="flex items-center justify-between gap-4 p-3 rounded-lg border bg-muted/30"
							>
								<div class="flex items-start gap-3">
									<Package class="h-5 w-5 text-muted-foreground shrink-0 mt-0.5" />
									<div class="space-y-0.5">
										<Label
											for="product-lifestyle-switch"
											class="text-sm font-medium cursor-pointer"
										>
											Generate Product Lifestyle Images
										</Label>
										<p class="text-xs text-muted-foreground">
											AI creates lifestyle scenes featuring your products
										</p>
									</div>
								</div>
								<Switch
									id="product-lifestyle-switch"
									bind:checked={useProductLifestyle}
									disabled={createMutation.isPending}
								/>
							</div>
						</div>
					{:else}
						<p class="text-sm text-muted-foreground">
							Upload your own images or leave empty to generate with AI
						</p>
					{/if}
				</div>
			</div>

			{#if error}
				<div class="text-sm text-destructive bg-destructive/10 p-3 rounded-lg">
					{error}
				</div>
			{/if}
		</div>

		<Dialog.Footer>
			<Button variant="outline" onclick={handleClose} disabled={createMutation.isPending}
				>Cancel</Button
			>
			<Button onclick={handleSubmit} disabled={createMutation.isPending}>
				{#if createMutation.isPending}
					<Loader2 class="mr-2 h-4 w-4 animate-spin" />
					Creating...
				{:else}
					<Sparkles class="mr-2 h-4 w-4" />
					Create Campaign
				{/if}
			</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
