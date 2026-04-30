<script setup lang="ts">
import { computed } from "vue";
import { useBrandDetailQuery } from "@/lib/brands/queries";
import { useUpdateBrandMutation } from "@/lib/brands/mutations";
import { useBrandSettingsForm } from "@/lib/brands/useBrandSettingsForm";
import { Button } from "@/components/ui/button";
import BrandGeneralSection from "./BrandGeneralSection.vue";
import BrandTargetAudiencesSection from "./BrandTargetAudiencesSection.vue";
import BrandContentPillarsSection from "./BrandContentPillarsSection.vue";

const props = defineProps<{
	brandId: string;
}>();

const { data: brand, isLoading, isError, error } = useBrandDetailQuery(() => props.brandId);

const { form, isDirty, discard, toRequest } = useBrandSettingsForm(brand);

const updateMutation = useUpdateBrandMutation();

const isSaving = computed(() => updateMutation.isPending.value);

const applyChanges = () => {
	updateMutation.mutate(
		{ id: props.brandId, body: toRequest() },
		{
			onSuccess: () => {
				discard();
			},
		},
	);
};
</script>

<template>
	<div class="pb-24 space-y-6">
		<div>
			<h1 class="text-xl font-semibold">Brand Settings</h1>
			<p class="text-sm text-muted-foreground mt-1">
				{{ brand?.name ?? (isLoading ? 'Loading…' : '') }}
			</p>
		</div>

		<div
			v-if="isError"
			class="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive"
		>
			{{ error instanceof Error ? error.message : 'Failed to load brand.' }}
		</div>

		<div class="grid gap-6">
			<BrandGeneralSection
				:form="form"
				:is-loading="isLoading"
			/>
			<BrandTargetAudiencesSection
				:audiences="form.target_audiences"
				:is-loading="isLoading"
			/>
			<BrandContentPillarsSection
				:pillars="form.content_pillars"
				:is-loading="isLoading"
			/>
		</div>
	</div>

	<Teleport to="body">
		<Transition name="footer-slide">
			<div
				v-if="isDirty"
				class="fixed bottom-0 inset-x-0 z-50 flex justify-center px-4 pb-4 pointer-events-none"
			>
				<div class="pointer-events-auto flex items-center gap-3 rounded-xl border border-border bg-background/95 backdrop-blur-sm px-4 py-3 shadow-lg ring-1 ring-black/5">
					<p class="text-sm text-muted-foreground">You have unsaved changes.</p>
					<div class="flex items-center gap-2">
						<Button
							variant="outline"
							size="sm"
							type="button"
							:disabled="isSaving"
							@click="discard"
						>
							Discard
						</Button>
						<Button
							variant="default"
							size="sm"
							type="button"
							:disabled="isSaving"
							@click="applyChanges"
						>
							{{ isSaving ? 'Saving…' : 'Apply changes' }}
						</Button>
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<style scoped>
.footer-slide-enter-active,
.footer-slide-leave-active {
	transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
}

.footer-slide-enter-from,
.footer-slide-leave-to {
	transform: translateY(100%);
	opacity: 0;
}
</style>
