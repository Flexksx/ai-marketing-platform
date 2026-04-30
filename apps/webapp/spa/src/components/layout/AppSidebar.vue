<script setup lang="ts">
import { computed, unref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { useAuthProvider } from "@/lib/auth/useAuth";
import { Button } from "@/components/ui/button";

const route = useRoute();
const { signOut } = useAuthProvider();
const isSigningOut = computed(() => unref(signOut.isPending));

const navItems = [
	{
		name: "calendar",
		label: "Calendar",
		to: { name: "calendar" },
	},
	{
		name: "brands",
		label: "Brands",
		to: { name: "brands" },
	},
] as const;

const isActive = (itemName: string) => {
	if (itemName === "brands") {
		return route.name === "brands" || route.name === "brand-settings";
	}
	return route.name === itemName;
};
</script>

<template>
	<aside class="flex h-svh w-56 shrink-0 flex-col border-r border-border bg-background">
		<div class="flex h-14 items-center border-b border-border px-4">
			<span class="text-sm font-semibold tracking-tight">AI Marketing</span>
		</div>

		<nav class="flex-1 overflow-y-auto px-2 py-3 space-y-0.5">
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
						'flex items-center gap-2.5 rounded-lg px-2.5 py-2 text-sm transition-colors',
						isActive(item.name)
							? 'bg-primary/10 text-primary font-medium'
							: 'text-muted-foreground hover:bg-muted hover:text-foreground',
					]"
					@click="navigate"
				>
					<svg
						v-if="item.name === 'calendar'"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 16 16"
						fill="currentColor"
						class="size-4 shrink-0"
					>
						<path d="M5.75 7.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM5 10.25a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0ZM10.25 7.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM9.5 10.25a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0ZM8 7.5a.75.75 0 1 0 0 1.5A.75.75 0 0 0 8 7.5ZM7.25 10.25a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0Z" />
						<path fill-rule="evenodd" d="M4.75 1a.75.75 0 0 0-.75.75V3a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2V1.75a.75.75 0 0 0-1.5 0V3h-5V1.75A.75.75 0 0 0 4.75 1ZM3.5 7a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v4.5a.5.5 0 0 1-.5.5H4a.5.5 0 0 1-.5-.5V7Z" clip-rule="evenodd" />
					</svg>
					<svg
						v-else-if="item.name === 'brands'"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 16 16"
						fill="currentColor"
						class="size-4 shrink-0"
					>
						<path fill-rule="evenodd" d="M4 4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1.5a.75.75 0 0 1-1.5 0V4a.5.5 0 0 0-.5-.5H6a.5.5 0 0 0-.5.5v1.5a.75.75 0 0 1-1.5 0V4Zm-2 5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9Z" clip-rule="evenodd" />
					</svg>
					{{ item.label }}
				</a>
			</RouterLink>
		</nav>

		<div class="border-t border-border px-2 py-3">
			<Button
				variant="ghost"
				size="sm"
				class="w-full justify-start gap-2.5 text-muted-foreground"
				:disabled="isSigningOut"
				@click="() => void signOut.mutateAsync()"
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4 shrink-0">
					<path fill-rule="evenodd" d="M2 4.75A2.75 2.75 0 0 1 4.75 2h3a2.75 2.75 0 0 1 2.75 2.75v.5a.75.75 0 0 1-1.5 0v-.5c0-.69-.56-1.25-1.25-1.25h-3c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h3c.69 0 1.25-.56 1.25-1.25v-.5a.75.75 0 0 1 1.5 0v.5A2.75 2.75 0 0 1 7.75 14h-3A2.75 2.75 0 0 1 2 11.25v-6.5Zm9.47.47a.75.75 0 0 1 1.06 0l2.25 2.25a.75.75 0 0 1 0 1.06l-2.25 2.25a.75.75 0 1 1-1.06-1.06l.97-.97H5.25a.75.75 0 0 1 0-1.5h7.19l-.97-.97a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
				</svg>
				{{ isSigningOut ? "Signing out…" : "Sign out" }}
			</Button>
		</div>
	</aside>
</template>
