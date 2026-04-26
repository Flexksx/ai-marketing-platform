<script setup lang="ts">
import { ref } from "vue";

import { useLogin } from "@/lib/auth/mutations";

const email = ref("");
const password = ref("");

const { mutateAsync, isPending, isError, error } = useLogin();

async function onSubmit() {
	try {
		await mutateAsync({ email: email.value, password: password.value });
	} catch {}
}
</script>

<template>
	<div class="mx-auto flex w-full max-w-sm flex-col gap-6 p-6">
		<div>
			<h1 class="text-2xl font-semibold tracking-tight">Sign in</h1>
			<p class="text-muted-foreground text-sm">Use your platform account</p>
		</div>

		<form class="flex flex-col gap-4" @submit.prevent="onSubmit">
			<div class="flex flex-col gap-1.5">
				<label class="text-sm font-medium" for="email">Email</label>
				<input
					id="email"
					v-model="email"
					type="email"
					autocomplete="email"
					required
					class="border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex h-9 w-full rounded-md border px-3 py-1 text-sm shadow-sm transition-all outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
				/>
			</div>
			<div class="flex flex-col gap-1.5">
				<label class="text-sm font-medium" for="password">Password</label>
				<input
					id="password"
					v-model="password"
					type="password"
					autocomplete="current-password"
					required
					class="border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex h-9 w-full rounded-md border px-3 py-1 text-sm shadow-sm transition-all outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
				/>
			</div>

			<p
				v-if="isError"
				class="text-destructive text-sm"
				role="alert"
			>
				{{
					(error as { response?: { data?: { message?: string } } })
						?.response?.data?.message ?? "Sign in failed"
				}}
			</p>

			<button
				type="submit"
				:disabled="isPending"
				class="ring-offset-background focus-visible:ring-ring inline-flex h-9 items-center justify-center rounded-md bg-zinc-900 px-4 text-sm font-medium text-zinc-50 transition-colors hover:bg-zinc-900/90 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
			>
				{{ isPending ? "Signing in…" : "Sign in" }}
			</button>
		</form>
	</div>
</template>
