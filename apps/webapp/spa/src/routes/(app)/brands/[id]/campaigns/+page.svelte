<script lang="ts">
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Button } from '$lib/components/ui/button';
	import { Trash2, FileText, Instagram, Linkedin } from 'lucide-svelte';
	import { page } from '$app/state';
	import * as Dialog from '$lib/components/ui/dialog';
	import { useCampaignsForBrand } from '$lib/api/campaign/queries';
	import { useDeleteCampaign } from '$lib/api/campaign/mutations';

	const brandId = $derived(page.params.id);

	const campaignsQuery = useCampaignsForBrand(
		() => brandId,
		() => ({ limit: 100, offset: 0, state: null })
	);

	const campaigns = $derived(campaignsQuery.data ?? []);
	const isLoadingCampaigns = $derived(campaignsQuery.isLoading);
	const campaignsError = $derived(campaignsQuery.error?.message ?? null);

	const deleteCampaignMutation = useDeleteCampaign();

	let deleteError = $state<string | null>(null);
	let showDeleteDialog = $state(false);
	let campaignToDelete = $state<string | null>(null);
	let isDeleting = $state(false);

	const handleDeleteClick = (campaignId: string) => {
		campaignToDelete = campaignId;
		showDeleteDialog = true;
		deleteError = null;
	};

	const handleDelete = () => {
		if (!brandId || !campaignToDelete) return;

		deleteError = null;
		isDeleting = true;

		deleteCampaignMutation.mutate(
			{
				brandId,
				campaignId: campaignToDelete
			},
			{
				onSuccess: () => {
					showDeleteDialog = false;
					campaignToDelete = null;
					isDeleting = false;
				},
				onError: (error) => {
					deleteError = error instanceof Error ? error.message : 'Failed to delete campaign';
					isDeleting = false;
				}
			}
		);
	};

	const getChannelIcon = (channel: string) => {
		if (channel === 'INSTAGRAM') return Instagram;
		if (channel === 'LINKEDIN') return Linkedin;
		return null;
	};

	const getChannelName = (channel: string): string => {
		if (channel === 'INSTAGRAM') return 'Instagram';
		if (channel === 'LINKEDIN') return 'LinkedIn';
		return channel;
	};
</script>

<div class="w-full h-full">
	<div class="w-[95%] max-w-[1200px] mx-auto px-8 py-8">
		<div class="mb-8">
			<h1 class="text-3xl font-bold text-foreground mb-2">Campaigns</h1>
			<p class="text-muted-foreground">Manage your marketing campaigns</p>
		</div>

		{#if deleteError}
			<div class="mb-4 p-4 bg-destructive/10 border border-destructive/20 rounded-md">
				<p class="text-sm text-destructive">{deleteError}</p>
			</div>
		{/if}

		{#if campaignsError}
			<div class="mb-4 p-4 bg-destructive/10 border border-destructive/20 rounded-md">
				<p class="text-sm text-destructive">Error loading campaigns: {campaignsError}</p>
			</div>
		{/if}

		{#if isLoadingCampaigns}
			<Card>
				<CardContent class="py-12 text-center">
					<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
					<p class="text-muted-foreground">Loading campaigns...</p>
				</CardContent>
			</Card>
		{:else if campaigns.length === 0}
			<Card>
				<CardContent class="py-12 text-center">
					<FileText class="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
					<p class="text-muted-foreground">No campaigns found</p>
				</CardContent>
			</Card>
		{:else}
			<div class="space-y-4">
				{#each campaigns as campaign}
					<Card class="hover:shadow-lg transition-shadow">
						<CardHeader>
							<div class="flex items-start justify-between">
								<div class="flex-1">
									<CardTitle class="text-xl mb-2">{campaign.data?.name || 'Untitled Campaign'}</CardTitle
									>
									{#if campaign.data?.description}
										<CardDescription class="text-base mt-2 line-clamp-3">
											{campaign.data.description}
										</CardDescription>
									{/if}
								</div>
								<Button
									variant="ghost"
									size="icon"
									class="text-destructive hover:text-destructive hover:bg-destructive/10"
									disabled={isDeleting}
									onclick={() => handleDeleteClick(campaign.id)}
								>
									{#if isDeleting}
										<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
									{:else}
										<Trash2 class="h-4 w-4" />
									{/if}
								</Button>
							</div>
						</CardHeader>
						<CardContent>
							<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
								<div class="flex items-center gap-2">
									<FileText class="h-4 w-4 text-muted-foreground" />
									<span class="text-sm text-muted-foreground">Duration:</span>
									<span class="text-sm font-medium">{campaign.data?.durationDays ?? 0} days</span>
								</div>

								<div class="flex items-center gap-2">
									<div class="flex flex-wrap gap-1">
										{#if campaign.data?.channels && campaign.data.channels.length > 0}
											{#each campaign.data.channels as channel}
												<Badge variant="secondary" class="text-xs flex items-center gap-1">
													{#if getChannelIcon(channel)}
														<svelte:component this={getChannelIcon(channel)} class="h-3 w-3" />
													{/if}
													{getChannelName(channel)}
												</Badge>
											{/each}
										{:else}
											<span class="text-sm text-muted-foreground">No channels</span>
										{/if}
									</div>
								</div>
							</div>
						</CardContent>
					</Card>
				{/each}
			</div>
		{/if}
	</div>
</div>

{#if showDeleteDialog && campaignToDelete}
	{@const campaign = campaigns.find((c) => c.id === campaignToDelete)}
	<Dialog.Root bind:open={showDeleteDialog}>
		<Dialog.Content>
			<Dialog.Header>
				<Dialog.Title>Delete Campaign</Dialog.Title>
				<Dialog.Description>
					Are you sure you want to delete "{campaign?.data?.name || 'this campaign'}"? This will
					permanently delete the campaign and all associated posts. This action cannot be undone.
				</Dialog.Description>
			</Dialog.Header>
			<Dialog.Footer>
				<Button
					variant="outline"
					onclick={() => (showDeleteDialog = false)}
					disabled={isDeleting}
				>
					Cancel
				</Button>
				<Button
					variant="destructive"
					onclick={handleDelete}
					disabled={isDeleting}
					class="gap-2"
				>
					{#if isDeleting}
						<div class="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
						Deleting...
					{:else}
						<Trash2 class="h-4 w-4" />
						Delete
					{/if}
				</Button>
			</Dialog.Footer>
		</Dialog.Content>
	</Dialog.Root>
{/if}
