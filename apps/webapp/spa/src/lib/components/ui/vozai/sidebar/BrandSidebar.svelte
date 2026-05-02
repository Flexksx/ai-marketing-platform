<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { useBrand, useBrands } from '$lib/resources/brands/queries';
	import { Avatar, AvatarFallback } from '$lib/components/ui/avatar';
	import {
		DropdownMenu,
		DropdownMenuContent,
		DropdownMenuItem,
		DropdownMenuSeparator,
		DropdownMenuTrigger
	} from '$lib/components/ui/dropdown-menu';
	import {
		Sidebar,
		SidebarContent,
		SidebarFooter,
		SidebarHeader,
		SidebarTrigger
	} from '$lib/components/ui/sidebar';
	import { sidebarMenuButtonVariants } from '$lib/components/ui/sidebar/sidebar-menu-button.svelte';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import { theme } from '$lib/stores/theme';
	import { cn } from '$lib/utils';
	import {
		Calendar,
		ChevronDown,
		LogOut,
		Megaphone,
		Monitor,
		Moon,
		Plus,
		Settings,
		Sun,
		User
	} from '@lucide/svelte';

	type BrandSidebarProps = {
		selectedBrandId: string | undefined;
	};

	let { selectedBrandId }: BrandSidebarProps = $props();

	const brandQuery = useBrand(() => selectedBrandId);
	const brandsQuery = useBrands();

	const brand = $derived(brandQuery.data ?? null);
	const brands = $derived(brandsQuery.data ?? []);
	const session = $derived(page.data.session);

	const navLinkClass = $derived(
		cn(
			sidebarMenuButtonVariants({ variant: 'default', size: 'default' }),
			'w-full text-muted-foreground/70 data-[active=true]:text-sidebar-accent-foreground'
		)
	);

	const calendarHref = $derived(
		selectedBrandId ? resolve(`/brands/${selectedBrandId}/posts_calendar`) : ''
	);
	const campaignsHref = $derived(
		selectedBrandId ? resolve(`/brands/${selectedBrandId}/campaigns`) : ''
	);
	const settingsHref = $derived(
		selectedBrandId ? resolve(`/brands/${selectedBrandId}/settings`) : ''
	);

	const isCalendarActive = $derived(!!calendarHref && page.url.pathname === calendarHref);
	const isCampaignsActive = $derived(!!campaignsHref && page.url.pathname === campaignsHref);
	const isSettingsActive = $derived(!!settingsHref && page.url.pathname === settingsHref);
</script>

<Sidebar collapsible="icon" variant="floating" class="brand-sidebar">
	<div
		class="bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border rounded-[2.5rem] shadow-lg h-full flex flex-col"
	>
		<SidebarHeader>
		<div class="flex items-center justify-center px-2 py-1.5">
			<SidebarTrigger />
		</div>
		{#if brand && brands.length > 0}
			<div class="px-2 pb-2 space-y-2">
				<DropdownMenu>
					<DropdownMenuTrigger
						class="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-accent group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0"
					>
						{#if brand.data?.logoUrl}
							<div
								class="flex h-6 w-6 items-center justify-center rounded-lg overflow-hidden bg-muted group-data-[collapsible=icon]:h-8 group-data-[collapsible=icon]:w-8"
							>
								<img
									src={brand.data.logoUrl}
									alt="{brand.name} logo"
									class="h-full w-full object-contain p-0.5"
								/>
							</div>
						{:else}
							<div
								class="bg-muted flex h-6 w-6 items-center justify-center rounded-lg group-data-[collapsible=icon]:h-8 group-data-[collapsible=icon]:w-8"
							>
								<span
									class="text-muted-foreground text-xs font-semibold group-data-[collapsible=icon]:text-sm"
								>
									{brand.name?.charAt(0)?.toUpperCase() ?? '?'}
								</span>
							</div>
						{/if}
						<div class="flex flex-1 flex-col items-start group-data-[collapsible=icon]:hidden">
							<span class="text-xs font-medium">{brand.name ?? 'Unnamed Brand'}</span>
							<span class="text-muted-foreground text-xs">Switch brand</span>
						</div>
						<ChevronDown
							class="h-4 w-4 text-muted-foreground group-data-[collapsible=icon]:hidden"
						/>
					</DropdownMenuTrigger>
					<DropdownMenuContent align="start" class="w-56">
						{#each brands as b (b.id)}
							<DropdownMenuItem class={b.id === selectedBrandId ? 'bg-accent' : ''}>
								<a
									href={resolve(`/brands/${b.id}`)}
									class="flex items-center gap-2 outline-hidden focus:outline-none [&:focus]:ring-2 [&:focus]:ring-sidebar-ring rounded-sm"
								>
									{#if b.data?.logoUrl}
										<div
											class="flex h-5 w-5 items-center justify-center rounded overflow-hidden bg-muted"
										>
											<img
												src={b.data.logoUrl}
												alt="{b.name} logo"
												class="h-full w-full object-contain p-0.5"
											/>
										</div>
									{:else}
										<div class="bg-muted flex h-5 w-5 items-center justify-center rounded">
											<span class="text-muted-foreground text-xs font-semibold">
												{b.name?.charAt(0)?.toUpperCase() ?? '?'}
											</span>
										</div>
									{/if}
									<span>{b.name ?? 'Unnamed Brand'}</span>
								</a>
							</DropdownMenuItem>
						{/each}
						<DropdownMenuSeparator />
						<DropdownMenuItem>
							<a
								href={resolve('/brands/create')}
								class="flex items-center gap-2 outline-hidden focus:outline-none [&:focus]:ring-2 [&:focus]:ring-sidebar-ring rounded-sm"
							>
								<Plus class="h-4 w-4" />
								<span>Create new brand</span>
							</a>
						</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
				{#if calendarHref}
					<Tooltip.Root>
						<Tooltip.Trigger>
							<a
								href={resolve(`/brands/${selectedBrandId}/posts_calendar`)}
								class={navLinkClass}
								data-active={isCalendarActive}
								data-slot="sidebar-menu-button"
								data-sidebar="menu-button"
							>
								<Calendar class="h-4 w-4" />
								<span class="group-data-[collapsible=icon]:hidden">Calendar</span>
							</a>
						</Tooltip.Trigger>
						<Tooltip.Content side="right" align="center">Posts Calendar</Tooltip.Content>
					</Tooltip.Root>
				{/if}
				{#if campaignsHref}
					<Tooltip.Root>
						<Tooltip.Trigger>
							<a
								href={resolve(`/brands/${selectedBrandId}/campaigns`)}
								class={navLinkClass}
								data-active={isCampaignsActive}
								data-slot="sidebar-menu-button"
								data-sidebar="menu-button"
							>
								<Megaphone class="h-4 w-4" />
								<span class="group-data-[collapsible=icon]:hidden">Campaigns</span>
							</a>
						</Tooltip.Trigger>
						<Tooltip.Content side="right" align="center">Campaigns</Tooltip.Content>
					</Tooltip.Root>
				{/if}
			</div>
		{/if}
	</SidebarHeader>
	<SidebarContent class="flex flex-col justify-between"></SidebarContent>
	{#if session}
		<SidebarFooter>
			<div class="px-2 space-y-2">
				{#if settingsHref}
					<Tooltip.Root>
						<Tooltip.Trigger>
							<a
								href={resolve(`/brands/${selectedBrandId}/settings`)}
								class={navLinkClass}
								data-active={isSettingsActive}
								data-slot="sidebar-menu-button"
								data-sidebar="menu-button"
							>
								<Settings class="h-4 w-4" />
								<span class="group-data-[collapsible=icon]:hidden">Settings</span>
							</a>
						</Tooltip.Trigger>
						<Tooltip.Content side="right" align="center">Settings</Tooltip.Content>
					</Tooltip.Root>
				{/if}
			</div>
			<div
				class="group-data-[collapsible=icon]:flex group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:w-full"
			>
				<DropdownMenu>
					<DropdownMenuTrigger>
						<Avatar class="cursor-pointer transition-opacity hover:opacity-80">
							<AvatarFallback>
								<User class="h-4 w-4" />
							</AvatarFallback>
						</Avatar>
					</DropdownMenuTrigger>
					<DropdownMenuContent align="end" class="w-48">
						<div class="px-2 py-1.5">
							<p class="text-muted-foreground text-xs font-medium">Theme</p>
						</div>
						<DropdownMenuItem onSelect={() => theme.set('light')}>
							<Sun class="h-4 w-4" />
							Light
						</DropdownMenuItem>
						<DropdownMenuItem onSelect={() => theme.set('dark')}>
							<Moon class="h-4 w-4" />
							Dark
						</DropdownMenuItem>
						<DropdownMenuItem onSelect={() => theme.set('system')}>
							<Monitor class="h-4 w-4" />
							System
						</DropdownMenuItem>
						<DropdownMenuSeparator />
						<DropdownMenuItem
							variant="destructive"
							onSelect={() => {
								const form = document.createElement('form');
								form.method = 'POST';
								form.action = '/login/logout';
								document.body.appendChild(form);
								form.submit();
							}}
						>
							<LogOut class="h-4 w-4" />
							Log out
						</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
			</div>
		</SidebarFooter>
	{/if}
	</div>
</Sidebar>

<style>
	:global(.brand-sidebar [data-slot='sidebar-inner']) {
		background-color: transparent;
		border: none;
		box-shadow: none;
	}

	:global(.ai-sparkles-gradient) {
		position: relative;
		overflow: hidden;
	}

	:global(.ai-sparkles-gradient::before) {
		content: '';
		position: absolute;
		top: 50%;
		left: 50%;
		width: 0;
		height: 0;
		border-radius: 50%;
		background: radial-gradient(
			circle,
			rgba(168, 85, 247, 0.6) 0%,
			rgba(139, 92, 246, 0.4) 30%,
			rgba(59, 130, 246, 0.2) 60%,
			transparent 100%
		);
		transform: translate(-50%, -50%);
		animation: pulse 3s ease-in-out infinite;
		pointer-events: none;
	}

	:global(.ai-sparkles-gradient:hover::before) {
		background: radial-gradient(
			circle,
			rgba(168, 85, 247, 0.7) 0%,
			rgba(139, 92, 246, 0.5) 30%,
			rgba(59, 130, 246, 0.3) 60%,
			transparent 100%
		);
	}

	:global(.ai-sparkles-gradient[data-active='true']::before) {
		background: radial-gradient(
			circle,
			rgba(168, 85, 247, 0.8) 0%,
			rgba(139, 92, 246, 0.6) 30%,
			rgba(59, 130, 246, 0.4) 60%,
			transparent 100%
		);
	}

	@keyframes pulse {
		0%,
		100% {
			width: 60px;
			height: 60px;
			opacity: 0.6;
		}
		50% {
			width: 80px;
			height: 80px;
			opacity: 0.8;
		}
	}
</style>
