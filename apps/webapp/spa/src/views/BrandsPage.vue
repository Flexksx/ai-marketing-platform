<script setup lang="ts">
import { useRouter } from "vue-router";
import { ChevronRight } from "lucide-vue-next";
import { useBrandsListQuery } from "@/lib/brands/queries";
import { Skeleton } from "@/components/ui/skeleton";

const router = useRouter();
const { data: brands, isLoading, isError, error } = useBrandsListQuery();

const openSettings = (brandId: string) => {
	void router.push({ name: "brand-settings", params: { brandId } });
};
</script>

<template>
	<div class="space-y-6">
		<div>
			<h1 class="text-xl font-semibold tracking-tight">Brands</h1>
			<p class="text-sm text-muted-foreground mt-1">Select a brand to manage its content strategy.</p>
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
							<ChevronRight class="size-3" />
						</div>
					</div>
				</button>
			</template>

			<div
				v-else
				class="col-span-full rounded-xl border border-dashed border-border p-8 text-center"
			>
				<p class="text-sm text-muted-foreground">No brands yet. Create one from the sidebar.</p>
			</div>
		</div>
	</div>
</template>
