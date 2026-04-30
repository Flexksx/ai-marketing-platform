<script setup lang="ts">
import { ref, computed, unref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ChevronsUpDown, Check, Plus } from "lucide-vue-next";
import { useBrandsListQuery } from "@/lib/brands/queries";
import { useCreateBrandMutation } from "@/lib/brands/mutations";
import {
	Popover,
	PopoverTrigger,
	PopoverContent,
} from "@/components/ui/popover";
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
const route = useRoute();

const { data: brands, isLoading } = useBrandsListQuery();

const activeBrandId = computed(() => route.params.brandId as string | undefined);

const activeBrand = computed(() =>
	brands.value?.find((b) => b.id === activeBrandId.value) ?? null,
);

const isPopoverOpen = ref(false);
const isCreateDialogOpen = ref(false);
const newBrandName = ref("");

const createMutation = useCreateBrandMutation();
const isCreating = computed(() => unref(createMutation.isPending));

const currentSubPage = computed(() => {
	if (route.name === "brand-calendar") return "brand-calendar";
	return "brand-settings";
});

const selectBrand = (brandId: string) => {
	isPopoverOpen.value = false;
	void router.push({ name: currentSubPage.value, params: { brandId } });
};

const openCreateDialog = () => {
	isPopoverOpen.value = false;
	newBrandName.value = "";
	createMutation.reset();
	isCreateDialogOpen.value = true;
};

const createBrand = async () => {
	if (!newBrandName.value.trim()) return;
	try {
		const result = await createMutation.mutateAsync({ name: newBrandName.value.trim() });
		isCreateDialogOpen.value = false;
		if (result.id) {
			void router.push({ name: "brand-settings", params: { brandId: result.id } });
		}
	} catch {
		/* mutation surfaces error */
	}
};
</script>

<template>
	<Popover v-model:open="isPopoverOpen">
		<PopoverTrigger as-child>
			<button
				type="button"
				class="flex h-14 w-full cursor-pointer items-center gap-2.5 border-b border-border px-4 transition-colors hover:bg-accent"
			>
				<div
					class="size-6 shrink-0 rounded-md flex items-center justify-center text-xs font-bold"
					:class="activeBrand ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'"
				>
					{{ activeBrand?.name ? activeBrand.name.charAt(0).toUpperCase() : '?' }}
				</div>
				<span
					class="flex-1 truncate text-left text-sm font-medium"
					:class="activeBrand ? 'text-foreground' : 'text-muted-foreground'"
				>
					{{ isLoading ? 'Loading…' : (activeBrand?.name ?? 'Select a brand') }}
				</span>
				<ChevronsUpDown class="size-3.5 shrink-0 text-muted-foreground" />
			</button>
		</PopoverTrigger>

		<PopoverContent side="right" align="start" class="w-60 p-1.5">
			<div v-if="brands && brands.length > 0" class="space-y-0.5 mb-1">
				<button
					v-for="brand in brands"
					:key="brand.id"
					type="button"
					class="flex w-full cursor-pointer items-center gap-2.5 rounded-md px-2.5 py-2 text-sm transition-colors hover:bg-accent"
					:class="brand.id === activeBrandId ? 'text-foreground' : 'text-muted-foreground hover:text-foreground'"
					@click="selectBrand(brand.id ?? '')"
				>
					<div
						class="size-5 shrink-0 rounded-md flex items-center justify-center text-[10px] font-bold"
						:class="brand.id === activeBrandId ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'"
					>
						{{ brand.name?.charAt(0).toUpperCase() ?? '?' }}
					</div>
					<span class="flex-1 truncate text-left">{{ brand.name }}</span>
					<Check v-if="brand.id === activeBrandId" class="size-3.5 shrink-0 text-primary" />
				</button>
			</div>

			<p v-else-if="!isLoading" class="px-2.5 py-2 text-xs text-muted-foreground">
				No brands yet.
			</p>

			<div class="border-t border-border pt-1 mt-1">
				<button
					type="button"
					class="flex w-full cursor-pointer items-center gap-2 rounded-md px-2.5 py-2 text-sm text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
					@click="openCreateDialog"
				>
					<Plus class="size-4 shrink-0" />
					New brand
				</button>
			</div>
		</PopoverContent>
	</Popover>

	<Dialog v-model:open="isCreateDialogOpen">
		<DialogContent class="max-w-sm">
			<DialogHeader>
				<DialogTitle>New brand</DialogTitle>
				<DialogDescription>Give your brand a name to get started. You can fill in the full details in settings.</DialogDescription>
			</DialogHeader>

			<form class="space-y-4" @submit.prevent="createBrand">
				<div class="grid gap-1.5">
					<label class="text-xs font-medium text-muted-foreground uppercase tracking-wide" for="brand-name-switcher">Name</label>
					<Input
						id="brand-name-switcher"
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
						@click="isCreateDialogOpen = false"
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
