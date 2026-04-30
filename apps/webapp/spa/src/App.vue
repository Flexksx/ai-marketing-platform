<script setup lang="ts">
import { RouterView } from "vue-router";
import LoginView from "./components/LoginView.vue";
import AppSidebar from "./components/layout/AppSidebar.vue";
import { useAuthProvider } from "./lib/auth/useAuth";

const { isAuthenticated } = useAuthProvider();
</script>

<template>
	<div v-if="!isAuthenticated" class="min-h-svh">
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
