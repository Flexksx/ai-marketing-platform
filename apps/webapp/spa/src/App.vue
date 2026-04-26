<script setup lang="ts">
import { provide } from "vue";
import LoginView from "./components/LoginView.vue";
import { authKey, useAuth } from "./lib/auth/useAuth";

const auth = useAuth();
provide(authKey, auth);
const { isAuthenticated, signOut, isLoggingOut } = auth;
</script>

<template>
	<div
		v-if="!isAuthenticated"
		class="min-h-svh"
	>
		<LoginView />
	</div>
	<div
		v-else
		class="bg-background min-h-svh"
	>
		<header
			class="border-border flex items-center justify-between border-b px-4 py-3"
		>
			<div class="text-sm text-zinc-600">Signed in</div>
			<button
				type="button"
				:disabled="isLoggingOut"
				class="ring-offset-background focus-visible:ring-ring inline-flex h-9 items-center justify-center rounded-md border border-zinc-200 bg-white px-4 text-sm font-medium shadow-sm transition-colors hover:bg-zinc-50 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50"
				@click="signOut()"
			>
				{{ isLoggingOut ? "Signing out…" : "Log out" }}
			</button>
		</header>
		<main class="p-6">
			<p class="text-muted-foreground text-sm">You are authenticated.</p>
		</main>
	</div>
</template>
