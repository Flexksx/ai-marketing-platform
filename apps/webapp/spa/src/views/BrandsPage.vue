<script setup lang="ts">
import { useRouter } from "vue-router";
import { useBrandsListQuery } from "@/lib/brands/queries";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
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
			<h1 class="text-xl font-semibold">Brands</h1>
			<p class="text-sm text-muted-foreground mt-1">Select a brand to manage its settings.</p>
		</div>

		<div
			v-if="isError"
			class="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive"
		>
			{{ error instanceof Error ? error.message : 'Failed to load brands.' }}
		</div>

		<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
			<template v-if="isLoading">
				<Skeleton v-for="n in 3" :key="n" class="h-20 rounded-xl" />
			</template>

			<template v-else-if="brands && brands.length > 0">
				<button
					v-for="brand in brands"
					:key="brand.id"
					type="button"
					class="text-left"
					@click="openSettings(brand.id ?? '')"
				>
					<Card class="h-full cursor-pointer transition-colors hover:bg-muted/50">
						<CardHeader>
							<CardTitle class="text-base">{{ brand.name }}</CardTitle>
							<CardDescription class="line-clamp-2">
								{{ brand.data?.description ?? 'No description.' }}
							</CardDescription>
						</CardHeader>
					</Card>
				</button>
			</template>

			<p
				v-else
				class="text-sm text-muted-foreground col-span-full"
			>
				No brands yet.
			</p>
		</div>
	</div>
</template>
