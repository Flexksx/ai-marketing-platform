<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Badge } from '$lib/components/ui/badge';
	import type { CampaignContentPlanItem } from '$lib/api/campaign-generation-jobs';
	import type { ChannelStrategyChannel } from '$lib/api/campaigns';
	import {
		contentFormatToLabel,
		contentTypeToLabel
	} from '$lib/api/brand-data/contentStrategyLabels';
	import PostPreviewInstagram from '$lib/components/ui/post-preview-instagram.svelte';
	import PostPreviewLinkedIn from '$lib/components/ui/post-preview-linkedin.svelte';
	import { Loader2, CheckCircle2, AlertCircle, Calendar } from 'lucide-svelte';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import {
		AlertDialog,
		AlertDialogAction,
		AlertDialogCancel,
		AlertDialogContent,
		AlertDialogDescription,
		AlertDialogFooter,
		AlertDialogHeader,
		AlertDialogTitle,
		AlertDialogTrigger
	} from '$lib/components/ui/alert-dialog';
	import {
		useUpdateContentPlanItem,
		useDeleteContentPlanItem
	} from '$lib/api/campaign-generation-jobs/mutations';

	type Props = {
		open?: boolean;
		selectedItem: CampaignContentPlanItem | null;
		brandName: string;
		brandId: string;
		jobId: string;
		onDeleted?: (itemId: string) => void;
	};

	let { open = $bindable(false), selectedItem, brandName, brandId, jobId, onDeleted }: Props = $props();
	let captionExpanded = $state(false);
	let editableCaption = $derived(selectedItem?.contentData?.caption ?? '');
	let editableScheduledAt = $derived<string>(
		selectedItem?.scheduledAt ? selectedItem.scheduledAt.slice(0, 16) : ''
	);

	const updateMutation = useUpdateContentPlanItem();
	const deleteMutation = useDeleteContentPlanItem();

	const getStatusBadge = (planItem: CampaignContentPlanItem) => {
		switch (planItem.generationStatus) {
			case 'completed':
				return {
					variant: 'outline' as const,
					class:
						'text-xs bg-green-50 dark:bg-green-950 border-green-300 dark:border-green-700 text-green-700 dark:text-green-300',
					icon: CheckCircle2,
					text: 'Post Ready'
				};
			case 'failed':
				return {
					variant: 'outline' as const,
					class:
						'text-xs bg-red-50 dark:bg-red-950 border-red-300 dark:border-red-700 text-red-700 dark:text-red-300',
					icon: AlertCircle,
					text: 'Failed'
				};
			default:
				return {
					variant: 'outline' as const,
					class:
						'text-xs bg-amber-50 dark:bg-amber-950 border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300',
					icon: Loader2,
					text: 'Generating...'
				};
		}
	};

	const formatDate = (dateString: string): string => {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-US', {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	};

	const statusBadge = $derived(selectedItem ? getStatusBadge(selectedItem) : null);
	const hasPost = $derived(selectedItem?.generationStatus === 'completed');
	const caption = $derived(
		hasPost && selectedItem ? editableCaption : (selectedItem?.contentData?.caption ?? '')
	);
	const isDirty = $derived(
		!selectedItem
			? false
			: editableCaption !== (selectedItem.contentData?.caption ?? '') ||
					editableScheduledAt !==
						(selectedItem.scheduledAt ? selectedItem.scheduledAt.slice(0, 16) : '')
	);
	const isSaving = $derived(updateMutation.isPending);
	const isDeleting = $derived(deleteMutation.isPending);
	const existingImageUrl = $derived(
		selectedItem?.imageUrls?.[0] ??
			(selectedItem?.contentData && 'image_url' in selectedItem.contentData
				? selectedItem.contentData.image_url
				: null)
	);
	const previewPost = $derived(
		selectedItem && hasPost && caption
			? {
					id: selectedItem.scheduledAt || 'preview',
					caption,
					image_url: existingImageUrl,
					channels: [selectedItem.channel as ChannelStrategyChannel]
				}
			: null
	);

	const handleSave = () => {
		if (!selectedItem) return;

		let scheduledAt: string | undefined;

		if (editableScheduledAt) {
			const scheduledDate = new Date(editableScheduledAt);
			if (!Number.isNaN(scheduledDate.getTime())) {
				scheduledAt = scheduledDate.toISOString();
			}
		}

		updateMutation.mutate({
			brandId,
			jobId,
			itemId: selectedItem.id,
			modification: {
				item_id: selectedItem.id,
				caption: editableCaption,
				scheduled_at: scheduledAt,
				image_url: existingImageUrl ?? undefined
			}
		});
	};

	const handleDelete = () => {
		if (!selectedItem || !brandId || !jobId) return;

		const deletedItemId = selectedItem.id;
		deleteMutation.mutate({
			brandId,
			jobId,
			itemId: deletedItemId
		}, {
			onSuccess: () => {
				open = false;
				onDeleted?.(deletedItemId);
			}
		});
	};
</script>

<Dialog.Root bind:open>
	<Dialog.Content
		class="!max-w-[60vw] w-[60vw] !max-h-[95vh] h-[95vh] flex flex-col overflow-hidden"
	>
		{#if selectedItem}
			<div class="flex-1 min-h-0 overflow-hidden">
				<div class="grid grid-cols-1 lg:grid-cols-5 gap-3 p-3 h-full">
					<div class="lg:col-span-3 space-y-2 overflow-y-auto pr-1">
						<div class="space-y-1">
							<div class="flex items-center justify-between gap-2">
								<Label class="text-sm font-medium">Description</Label>
								{#if statusBadge}
									<Badge variant={statusBadge.variant} class={statusBadge.class}>
										<statusBadge.icon
											class="w-3 h-3 mr-1 {statusBadge.icon === Loader2 ? 'animate-spin' : ''}"
										/>
										{statusBadge.text}
									</Badge>
								{/if}
							</div>
							<div
								class="p-2 bg-muted/50 rounded-md border text-sm text-muted-foreground min-h-[52px] whitespace-pre-wrap"
							>
								{selectedItem.description}
							</div>
							<div class="flex flex-wrap gap-1.5">
								<Badge variant="secondary" class="rounded-full font-normal">
									{contentFormatToLabel(selectedItem.contentFormat)}
								</Badge>
								<Badge variant="secondary" class="rounded-full font-normal">
									{contentTypeToLabel(selectedItem.contentType)}
								</Badge>
							</div>
						</div>

						<div class="space-y-1">
							<Label class="text-sm font-medium flex items-center gap-2">
								<Calendar class="w-4 h-4" />
								Scheduled
							</Label>
							<div class="space-y-1">
								<Input
									type="datetime-local"
									bind:value={editableScheduledAt}
									class="w-full"
									disabled={isSaving || isDeleting}
								/>
								<p class="text-xs text-muted-foreground">
									Current: {formatDate(selectedItem.scheduledAt)}
								</p>
							</div>
						</div>

						{#if hasPost}
							<div class="space-y-1">
								<div class="flex items-center justify-between gap-2">
									<Label class="text-sm font-medium">Caption</Label>
									<button
										type="button"
										class="text-xs text-muted-foreground hover:text-foreground cursor-pointer"
										onclick={() => (captionExpanded = !captionExpanded)}
									>
										{captionExpanded ? 'Collapse' : 'Expand'}
									</button>
								</div>
								<div
									class="p-2 bg-muted/50 rounded-md border text-sm text-muted-foreground whitespace-pre-wrap {captionExpanded
										? 'min-h-[120px]'
										: 'max-h-[4.5rem] overflow-hidden'}"
								>
									<Textarea
										id="caption"
										bind:value={editableCaption}
										class="min-h-[80px] resize-none bg-transparent border-0 p-0 shadow-none focus-visible:ring-0 focus-visible:border-0"
										disabled={isSaving || isDeleting}
									/>
								</div>
							</div>
						{:else if selectedItem.generationStatus !== 'completed'}
							<div
								class="border rounded-lg p-4 flex flex-col items-center justify-center text-center"
							>
								<Loader2 class="w-10 h-10 text-primary animate-spin mb-2" />
								<h3 class="text-sm font-semibold mb-1">Generating Post</h3>
								<p class="text-xs text-muted-foreground">This post is being created...</p>
							</div>
						{/if}
					</div>

					<div class="lg:col-span-2 space-y-2 overflow-y-auto">
						{#if previewPost && hasPost}
							<div class="space-y-1">
								<Label class="text-sm font-medium">Post Preview</Label>
								<div class="flex justify-center pb-1">
									{#if selectedItem.channel === 'INSTAGRAM'}
										<PostPreviewInstagram post={previewPost} />
									{:else if selectedItem.channel === 'LINKEDIN'}
										<PostPreviewLinkedIn post={previewPost} />
									{/if}
								</div>
							</div>
						{:else}
							<div
								class="border rounded-lg p-4 flex flex-col items-center justify-center text-center h-full"
							>
								<Calendar class="w-8 h-8 text-muted-foreground mb-2" />
								<h3 class="text-base font-semibold mb-1">No Preview Available</h3>
								<p class="text-sm text-muted-foreground">
									Preview will appear once post generation is complete
								</p>
							</div>
						{/if}
					</div>
				</div>
			</div>
			<div class="flex items-center justify-between px-3 pb-3 pt-2 border-t mt-2">
				<div class="flex items-center">
					<AlertDialog>
						<AlertDialogTrigger asChild>
							<Button
								variant="ghost"
								class="text-destructive cursor-pointer"
								disabled={isDeleting || isSaving}
							>
								Delete
							</Button>
						</AlertDialogTrigger>
						<AlertDialogContent>
							<AlertDialogHeader>
								<AlertDialogTitle>Delete content plan item</AlertDialogTitle>
								<AlertDialogDescription>
									This action cannot be undone. This will permanently delete this content plan item
									scheduled for {formatDate(selectedItem.scheduledAt)} on{' '}
									{selectedItem.channel.toLowerCase()}.
								</AlertDialogDescription>
							</AlertDialogHeader>
							<AlertDialogFooter>
								<AlertDialogCancel class="cursor-pointer" disabled={isDeleting}>
									Cancel
								</AlertDialogCancel>
								<AlertDialogAction
									class="cursor-pointer"
									disabled={isDeleting}
									onclick={handleDelete}
								>
									{#if isDeleting}
										<Loader2 class="h-4 w-4 animate-spin" />
										Deleting...
									{:else}
										Delete
									{/if}
								</AlertDialogAction>
							</AlertDialogFooter>
						</AlertDialogContent>
					</AlertDialog>
				</div>
				<Button class="cursor-pointer" disabled={isSaving || isDeleting} onclick={handleSave}>
					{#if isSaving}
						<Loader2 class="h-4 w-4 animate-spin mr-2" />
						Saving...
					{:else}
						Save
					{/if}
				</Button>
			</div>
		{/if}
	</Dialog.Content>
</Dialog.Root>
