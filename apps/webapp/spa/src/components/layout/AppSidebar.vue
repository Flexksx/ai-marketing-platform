<script setup lang="ts">
import { computed, unref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { CalendarDays, LogOut, Settings2 } from "lucide-vue-next";
import { useAuthProvider } from "@/lib/auth/useAuth";
import { Button } from "@/components/ui/button";
import BrandSwitcher from "./BrandSwitcher.vue";

const route = useRoute();
const { signOut } = useAuthProvider();
const isSigningOut = computed(() => unref(signOut.isPending));

const activeBrandId = computed(() => route.params.brandId as string | undefined);

const navItems = computed(() => {
	if (!activeBrandId.value) return [];
	return [
		{
			name: "brand-calendar" as const,
			label: "Calendar",
			to: { name: "brand-calendar", params: { brandId: activeBrandId.value } },
		},
		{
			name: "brand-settings" as const,
			label: "My Brand",
			to: { name: "brand-settings", params: { brandId: activeBrandId.value } },
		},
	];
});

const isActive = (name: string) => route.name === name;
</script>

<template>
	<aside class="flex h-svh w-52 shrink-0 flex-col border-r border-border bg-sidebar">
		<!-- Brand picker — acts as the header -->
		<BrandSwitcher />

		<!-- Nav -->
		<nav class="flex-1 overflow-y-auto px-2 py-3 space-y-0.5">
			<template v-if="navItems.length > 0">
				<RouterLink
					v-for="item in navItems"
					:key="item.name"
					:to="item.to"
					custom
					v-slot="{ navigate, href }"
				>
					<a
						:href="href"
						:class="[
							'flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-sm transition-colors cursor-pointer',
							isActive(item.name)
								? 'bg-primary/10 text-primary font-medium'
								: 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
						]"
						@click="navigate"
					>
						<CalendarDays v-if="item.name === 'brand-calendar'" class="size-4 shrink-0" />
						<Settings2 v-else-if="item.name === 'brand-settings'" class="size-4 shrink-0" />
						{{ item.label }}
					</a>
				</RouterLink>
			</template>

			<p v-else class="px-2.5 py-2 text-xs text-muted-foreground/60">
				Select a brand to continue.
			</p>
		</nav>

		<!-- Footer -->
		<div class="border-t border-border px-2 py-3">
			<Button
				variant="ghost"
				size="sm"
				class="w-full justify-start gap-2.5 text-muted-foreground hover:text-foreground cursor-pointer"
				:disabled="isSigningOut"
				@click="() => void signOut.mutateAsync()"
			>
				<LogOut class="size-4 shrink-0" />
				{{ isSigningOut ? "Signing out…" : "Sign out" }}
			</Button>
		</div>
	</aside>
</template>
