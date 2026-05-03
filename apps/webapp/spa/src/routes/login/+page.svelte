<script lang="ts">
	import { goto } from '$app/navigation';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import { Eye, EyeOff } from '@lucide/svelte';
	import { loginWithEmailPassword, signupWithEmailPassword } from '$lib/supabase/browser-auth';

	let isSignup = $state(false);
	let showPassword = $state(false);
	let showConfirmPassword = $state(false);

	let email = $state('');
	let passwordValue = $state('');
	let confirmPasswordValue = $state('');

	let errorMessage = $state<string | null>(null);
	let successMessage = $state<string | null>(null);
	let isPending = $state(false);

	function toggleMode() {
		isSignup = !isSignup;
		showPassword = false;
		showConfirmPassword = false;
		passwordValue = '';
		confirmPasswordValue = '';
		errorMessage = null;
		successMessage = null;
	}

	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}

	function toggleConfirmPasswordVisibility() {
		showConfirmPassword = !showConfirmPassword;
	}

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		errorMessage = null;
		successMessage = null;
		isPending = true;

		try {
			const result = isSignup
				? await signupWithEmailPassword(email, passwordValue, confirmPasswordValue)
				: await loginWithEmailPassword(email, passwordValue);

			if (!result.ok) {
				errorMessage = result.error;
				return;
			}

			if ('message' in result && result.message) {
				successMessage = result.message;
				return;
			}

			await goto('/');
		} finally {
			isPending = false;
		}
	}
</script>

<svelte:head>
	<title>{isSignup ? 'Sign Up' : 'Login'} - Voz AI</title>
</svelte:head>

<div
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 px-4 dark:from-slate-900 dark:to-slate-800"
>
	<div class="w-full max-w-md">
		<!-- Welcome Header -->
		<div class="mb-8 text-center">
			<h1 class="mb-2 text-4xl font-bold text-slate-900 dark:text-slate-100">Welcome to Voz AI</h1>
			<p class="text-slate-600 dark:text-slate-400">
				{isSignup ? 'Create your account to get started' : 'Sign in to your account'}
			</p>
		</div>

		<!-- Login/Signup Card -->
		<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm dark:bg-slate-800/80">
			<CardHeader class="pb-4 text-center">
				<CardTitle class="text-2xl font-semibold">
					{isSignup ? 'Create Account' : 'Sign In'}
				</CardTitle>
			</CardHeader>

			<CardContent class="space-y-6">
				{#if errorMessage}
					<div
						class="rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20"
					>
						<p class="text-sm font-medium text-red-800 dark:text-red-200">
							{errorMessage}
						</p>
					</div>
				{/if}

				{#if successMessage}
					<div
						class="rounded-lg border border-green-200 bg-green-50 p-4 dark:border-green-800 dark:bg-green-900/20"
					>
						<p class="text-sm font-medium text-green-800 dark:text-green-200">
							{successMessage}
						</p>
					</div>
				{/if}

				<form onsubmit={handleSubmit}>
					<div class="space-y-4">
						<!-- Email Field -->
						<div class="space-y-2">
							<Label for="email" class="text-sm font-medium">Email</Label>
							<Input
								id="email"
								name="email"
								type="email"
								placeholder="Enter your email"
								bind:value={email}
								required
								class="h-11"
							/>
						</div>

						<!-- Password Field -->
						<div class="space-y-2">
							<Label for="password" class="text-sm font-medium">Password</Label>
							<div class="relative">
								<Input
									id="password"
									name="password"
									bind:value={passwordValue}
									type={showPassword ? 'text' : 'password'}
									placeholder="Enter your password"
									required
									class="h-11 pr-10"
									autocomplete={isSignup ? 'new-password' : 'current-password'}
								/>
								<button
									type="button"
									onclick={togglePasswordVisibility}
									class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
									aria-label={showPassword ? 'Hide password' : 'Show password'}
									tabindex="-1"
								>
									{#if showPassword}
										<EyeOff class="h-5 w-5" />
									{:else}
										<Eye class="h-5 w-5" />
									{/if}
								</button>
							</div>
							{#if isSignup}
								<p class="text-xs text-slate-500 dark:text-slate-400">
									Password must be at least 8 characters with uppercase, lowercase, numbers, and
									special characters.
								</p>
							{/if}
						</div>

						<!-- Confirm Password Field (only for signup) -->
						{#if isSignup}
							<div class="space-y-2">
								<Label for="confirmPassword" class="text-sm font-medium">Confirm Password</Label>
								<div class="relative">
									<Input
										id="confirmPassword"
										name="confirmPassword"
										bind:value={confirmPasswordValue}
										type={showConfirmPassword ? 'text' : 'password'}
										placeholder="Confirm your password"
										required
										class="h-11 pr-10"
										autocomplete="new-password"
									/>
									<button
										type="button"
										onclick={toggleConfirmPasswordVisibility}
										class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
										aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
										tabindex="-1"
									>
										{#if showConfirmPassword}
											<EyeOff class="h-5 w-5" />
										{:else}
											<Eye class="h-5 w-5" />
										{/if}
									</button>
								</div>
							</div>
						{/if}

						<!-- Submit Button -->
						<Button
							type="submit"
							class="h-11 w-full text-base font-medium"
							variant="default"
							disabled={isPending}
						>
							{#if isPending}
								{isSignup ? 'Creating account...' : 'Signing in...'}
							{:else}
								{isSignup ? 'Create Account' : 'Sign In'}
							{/if}
						</Button>
					</div>
				</form>

				<!-- Separator -->
				<div class="relative">
					<Separator class="my-6" />
					<div class="absolute inset-0 flex items-center justify-center">
						<span
							class="bg-white px-3 text-sm text-slate-500 dark:bg-slate-800 dark:text-slate-400"
						>
							or
						</span>
					</div>
				</div>

				<!-- Toggle Mode Button -->
				<div class="text-center">
					<Button
						variant="ghost"
						onclick={toggleMode}
						class="text-sm text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100"
					>
						{isSignup ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
					</Button>
				</div>
			</CardContent>
		</Card>

		<!-- Footer -->
		<div class="mt-8 text-center">
			<p class="text-sm text-slate-500 dark:text-slate-400">
				By {isSignup ? 'creating an account' : 'signing in'}, you agree to our
				<button type="button" class="text-primary hover:underline">Terms of Service</button>
				and
				<button type="button" class="text-primary hover:underline">Privacy Policy</button>
			</p>
		</div>
	</div>
</div>
