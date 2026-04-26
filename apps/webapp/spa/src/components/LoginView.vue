<script setup lang="ts">
import { computed, ref, unref } from "vue";

import { useAuth } from "@/lib/auth/useAuth";

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const isRegisterMode = ref(false);

const { signIn, signUp } = useAuth();

const isSubmitting = computed(
	() =>
		(isRegisterMode.value && unref(signUp.isPending)) ||
		(!isRegisterMode.value && unref(signIn.isPending)),
);

const displayError = computed(() => {
	if (isRegisterMode.value && unref(signUp.isError)) {
		return unref(signUp.error);
	}
	if (!isRegisterMode.value && unref(signIn.isError)) {
		return unref(signIn.error);
	}
	return null;
});

type Axiosish = { response?: { data?: { message?: string } } } | null;

function errorText(err: unknown, fallback: string) {
	return (
		((err as Axiosish) ?? null)?.response?.data?.message?.trim() || fallback
	);
}

async function onSubmit() {
	try {
		const body = { email: email.value, password: password.value };
		if (isRegisterMode.value) {
			await signUp.mutateAsync(body);
		} else {
			await signIn.mutateAsync(body);
		}
	} catch {
		/* mutation surfaces error */
	}
}
</script>

<template>
	<div class="mx-auto flex w-full max-w-sm flex-col gap-6 p-6">
		<div>
			<h1 class="text-2xl font-semibold tracking-tight">
				{{ isRegisterMode ? "Create account" : "Sign in" }}
			</h1>
			<p class="text-muted-foreground text-sm">
				{{
					isRegisterMode
						? "Set your email and password to get started"
						: "Use your platform account"
				}}
			</p>
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
				<div
					class="border-input bg-background ring-offset-background focus-within:ring-ring relative flex h-9 w-full rounded-md border shadow-sm transition-all focus-within:ring-2 focus-within:ring-offset-2"
				>
					<input
						id="password"
						v-model="password"
						:type="showPassword ? 'text' : 'password'"
						:autocomplete="isRegisterMode ? 'new-password' : 'current-password'"
						required
						class="placeholder:text-muted-foreground min-w-0 flex-1 rounded-md border-0 bg-transparent px-3 py-1 pr-2 text-sm outline-none"
					/>
					<button
						type="button"
						:aria-pressed="showPassword"
						class="text-muted-foreground hover:text-foreground shrink-0 rounded-r-md px-3 text-xs font-medium"
						@click="showPassword = !showPassword"
					>
						{{ showPassword ? "Hide" : "Show" }}
					</button>
				</div>
			</div>

			<p
				v-if="displayError"
				class="text-destructive text-sm"
				role="alert"
			>
				{{
					errorText(
						displayError,
						isRegisterMode
							? "Could not create account"
							: "Sign in failed",
					)
				}}
			</p>

			<button
				type="submit"
				:disabled="isSubmitting"
				class="ring-offset-background focus-visible:ring-ring inline-flex h-9 items-center justify-center rounded-md bg-zinc-900 px-4 text-sm font-medium text-zinc-50 transition-colors hover:bg-zinc-900/90 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
			>
				<template v-if="isRegisterMode">
					{{ signUp.isPending ? "Creating account…" : "Create account" }}
				</template>
				<template v-else>
					{{ signIn.isPending ? "Signing in…" : "Sign in" }}
				</template>
			</button>

			<p class="text-center text-sm text-zinc-600">
				<template v-if="isRegisterMode">
					Already have an account?
					<button
						type="button"
						class="text-zinc-900 underline underline-offset-2 hover:text-zinc-700"
						@click="isRegisterMode = false"
					>
						Sign in
					</button>
				</template>
				<template v-else>
					No account?
					<button
						type="button"
						class="text-zinc-900 underline underline-offset-2 hover:text-zinc-700"
						@click="isRegisterMode = true"
					>
						Create one
					</button>
				</template>
			</p>
		</form>
	</div>
</template>
