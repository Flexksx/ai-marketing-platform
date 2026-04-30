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
	<div class="relative z-10 w-full max-w-sm px-4">
		<!-- Glass card -->
		<div class="glass rounded-2xl px-8 py-8 shadow-xl shadow-primary/5">
			<!-- Brand -->
			<div class="mb-7">
				<div class="mb-5">
					<div class="size-7 rounded-md bg-primary flex items-center justify-center">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-4 text-primary-foreground">
							<path d="M8.5 2.75a.75.75 0 0 0-1.5 0v5.19L5.03 5.97a.75.75 0 0 0-1.06 1.06l3.5 3.5a.75.75 0 0 0 1.06 0l3.5-3.5a.75.75 0 0 0-1.06-1.06L8.5 7.94V2.75Z" />
							<path d="M3.25 13a.75.75 0 0 0 0 1.5h9.5a.75.75 0 0 0 0-1.5h-9.5Z" />
						</svg>
					</div>
				</div>
				<h1 class="text-xl font-semibold tracking-tight text-foreground">
					{{ isRegisterMode ? "Create account" : "Welcome back" }}
				</h1>
				<p class="text-sm text-muted-foreground mt-1">
					{{
						isRegisterMode
							? "Set your email and password to get started"
							: "Sign in to your account"
					}}
				</p>
			</div>

			<form class="flex flex-col gap-4" @submit.prevent="onSubmit">
				<div class="flex flex-col gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide" for="email">Email</label>
					<input
						id="email"
						v-model="email"
						type="email"
						autocomplete="email"
						required
						class="border-input bg-background/80 ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex h-9 w-full rounded-lg border px-3 py-1 text-sm shadow-sm transition-all outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
					/>
				</div>
				<div class="flex flex-col gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide" for="password">Password</label>
					<div
						class="border-input bg-background/80 ring-offset-background focus-within:ring-ring relative flex h-9 w-full rounded-lg border shadow-sm transition-all focus-within:ring-2 focus-within:ring-offset-2"
					>
						<input
							id="password"
							v-model="password"
							:type="showPassword ? 'text' : 'password'"
							:autocomplete="isRegisterMode ? 'new-password' : 'current-password'"
							required
							class="placeholder:text-muted-foreground min-w-0 flex-1 rounded-lg border-0 bg-transparent px-3 py-1 pr-2 text-sm outline-none"
						/>
						<button
							type="button"
							:aria-pressed="showPassword"
							class="text-muted-foreground hover:text-foreground shrink-0 rounded-r-lg px-3 text-xs font-medium transition-colors cursor-pointer"
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
					class="ring-offset-background focus-visible:ring-ring mt-1 inline-flex h-9 cursor-pointer items-center justify-center rounded-lg bg-primary px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
				>
					<template v-if="isRegisterMode">
						{{ signUp.isPending ? "Creating account…" : "Create account" }}
					</template>
					<template v-else>
						{{ signIn.isPending ? "Signing in…" : "Sign in" }}
					</template>
				</button>

				<p class="text-center text-sm text-muted-foreground">
					<template v-if="isRegisterMode">
						Already have an account?
						<button
							type="button"
							class="text-primary underline underline-offset-2 hover:text-primary/80 cursor-pointer"
							@click="isRegisterMode = false"
						>
							Sign in
						</button>
					</template>
					<template v-else>
						No account?
						<button
							type="button"
							class="text-primary underline underline-offset-2 hover:text-primary/80 cursor-pointer"
							@click="isRegisterMode = true"
						>
							Create one
						</button>
					</template>
				</p>
			</form>
		</div>
	</div>
</template>
