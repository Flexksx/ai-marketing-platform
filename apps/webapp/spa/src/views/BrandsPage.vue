<script setup lang="ts">
import { ref, computed, unref } from "vue";
import { useRouter } from "vue-router";
import { useBrandsListQuery } from "@/lib/brands/queries";
import { useCreateBrandMutation } from "@/lib/brands/mutations";
import { Skeleton } from "@/components/ui/skeleton";
import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
	DialogDescription,
	DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";

const router = useRouter();
const { data: brands, isLoading, isError, error } = useBrandsListQuery();

const openSettings = (brandId: string) => {
	void router.push({ name: "brand-settings", params: { brandId } });
};

const isDialogOpen = ref(false);
const newBrandName = ref("");

const createMutation = useCreateBrandMutation();
const isCreating = computed(() => unref(createMutation.isPending));

const openDialog = () => {
	newBrandName.value = "";
	createMutation.reset();
	isDialogOpen.value = true;
};

const createBrand = async () => {
	if (!newBrandName.value.trim()) return;
	try {
		const result = await createMutation.mutateAsync({ name: newBrandName.value.trim() });
		isDialogOpen.value = false;
		if (result.id) {
			void router.push({ name: "brand-settings", params: { brandId: result.id } });
		}
	} catch {
		/* mutation surfaces error */
	}
};
</script>

<template>
	<div class="space-y-6">
		<div class="flex items-start justify-between gap-3">
			<div>
				<h1 class="text-xl font-semibold tracking-tight">Brands</h1>
				<p class="text-sm text-muted-foreground mt-1">Select a brand to manage its content strategy.</p>
			</div>
			<button
				type="button"
				class="inline-flex cursor-pointer items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground transition-colors hover:bg-primary/90 shrink-0"
				@click="openDialog"
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-3.5">
					<path d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z" />
				</svg>
				New brand
			</button>
		</div>

		<div
			v-if="isError"
			class="rounded-xl border border-destructive/30 bg-destructive/8 px-4 py-3 text-sm text-destructive"
		>
			{{ error instanceof Error ? error.message : 'Failed to load brands.' }}
		</div>

		<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
			<template v-if="isLoading">
				<Skeleton v-for="n in 3" :key="n" class="h-24 rounded-xl" />
			</template>

			<template v-else-if="brands && brands.length > 0">
				<button
					v-for="brand in brands"
					:key="brand.id"
					type="button"
					class="group text-left cursor-pointer"
					@click="openSettings(brand.id ?? '')"
				>
					<div class="relative h-full rounded-xl border border-border bg-card p-4 transition-all duration-150 hover:border-primary/30 hover:shadow-md hover:shadow-primary/5 hover:-translate-y-px">
						<div class="absolute top-0 left-4 right-4 h-px rounded-full bg-gradient-to-r from-transparent via-primary/20 to-transparent transition-opacity duration-150 group-hover:via-primary/50" />
						<div class="space-y-1.5">
							<p class="text-sm font-semibold tracking-tight text-foreground">{{ brand.name }}</p>
							<p class="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
								{{ brand.data?.description ?? 'No description yet.' }}
							</p>
						</div>
						<div class="mt-3 flex items-center gap-1 text-xs text-primary opacity-0 transition-opacity duration-150 group-hover:opacity-100">
							<span>Open settings</span>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="size-3">
								<path fill-rule="evenodd" d="M6.22 4.22a.75.75 0 0 1 1.06 0l3.25 3.25a.75.75 0 0 1 0 1.06l-3.25 3.25a.75.75 0 0 1-1.06-1.06L8.94 8 6.22 5.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
							</svg>
						</div>
					</div>
				</button>
			</template>

			<div
				v-else
				class="col-span-full rounded-xl border border-dashed border-border p-8 text-center"
			>
				<p class="text-sm text-muted-foreground">No brands yet.</p>
			</div>
		</div>
	</div>

	<!-- Create brand dialog -->
	<Dialog v-model:open="isDialogOpen">
		<DialogContent class="max-w-sm">
			<DialogHeader>
				<DialogTitle>New brand</DialogTitle>
				<DialogDescription>Give your brand a name to get started. You can fill in the full details in settings.</DialogDescription>
			</DialogHeader>

			<form class="space-y-4" @submit.prevent="createBrand">
				<div class="grid gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide" for="brand-name">Name</label>
					<Input
						id="brand-name"
						v-model="newBrandName"
						placeholder="Brand name"
						:disabled="isCreating"
						required
						autofocus
					/>
				</div>

				<p v-if="createMutation.isError.value" class="text-destructive text-sm" role="alert">
					{{ createMutation.error.value instanceof Error ? createMutation.error.value.message : 'Could not create brand.' }}
				</p>

				<DialogFooter>
					<button
						type="button"
						class="inline-flex cursor-pointer items-center justify-center rounded-lg border border-border bg-background px-3 py-1.5 text-sm transition-colors hover:bg-muted disabled:pointer-events-none disabled:opacity-50"
						:disabled="isCreating"
						@click="isDialogOpen = false"
					>
						Cancel
					</button>
					<button
						type="submit"
						class="inline-flex cursor-pointer items-center justify-center rounded-lg bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
						:disabled="isCreating || !newBrandName.trim()"
					>
						{{ isCreating ? 'Creating…' : 'Create brand' }}
					</button>
				</DialogFooter>
			</form>
		</DialogContent>
	</Dialog>
</template>
