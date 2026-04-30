<script setup lang="ts">
import { RouterView } from "vue-router";
import LoginView from "./components/LoginView.vue";
import AppSidebar from "./components/layout/AppSidebar.vue";
import { useAuthProvider } from "./lib/auth/useAuth";

const { isAuthenticated } = useAuthProvider();
</script>

<template>
	<div v-if="!isAuthenticated" class="min-h-svh bg-background relative overflow-hidden flex items-center justify-center">
		<!-- Subtle background gradient orbs -->
		<div class="pointer-events-none absolute inset-0 overflow-hidden">
			<div class="absolute -top-32 -left-32 size-96 rounded-full bg-primary/8 blur-3xl" />
			<div class="absolute -bottom-32 -right-32 size-96 rounded-full bg-primary/6 blur-3xl" />
			<div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 size-[600px] rounded-full bg-primary/4 blur-3xl" />
		</div>
		<LoginView />
	</div>

	<div v-else class="bg-background flex min-h-svh">
		<AppSidebar />
		<main class="flex-1 overflow-y-auto p-6">
			<div class="mx-auto max-w-4xl">
				<RouterView />
			</div>
		</main>
	</div>
</template>
