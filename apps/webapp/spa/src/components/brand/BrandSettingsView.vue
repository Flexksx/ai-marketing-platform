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
	<div class="pb-28 space-y-6">
		<!-- Page header -->
		<div class="space-y-0.5">
			<h1 class="text-xl font-semibold tracking-tight">Brand Settings</h1>
			<p class="text-sm text-muted-foreground">
				{{ brand?.name ?? (isLoading ? 'Loading…' : 'Configure your brand identity and content strategy.') }}
			</p>
		</div>

		<div
			v-if="isError"
			class="rounded-xl border border-destructive/30 bg-destructive/8 px-4 py-3 text-sm text-destructive"
		>
			{{ error instanceof Error ? error.message : 'Failed to load brand.' }}
		</div>

		<div class="grid gap-4">
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
				class="fixed bottom-0 inset-x-0 z-50 flex justify-center px-4 pb-5 pointer-events-none"
			>
				<div class="pointer-events-auto flex items-center gap-3 rounded-2xl glass px-5 py-3 shadow-xl shadow-primary/10">
					<div class="size-1.5 rounded-full bg-amber-400 shrink-0" />
					<p class="text-sm text-muted-foreground">Unsaved changes</p>
					<div class="flex items-center gap-2 ml-1">
						<Button
							variant="outline"
							size="sm"
							type="button"
							class="h-7 cursor-pointer"
							:disabled="isSaving"
							@click="discard"
						>
							Discard
						</Button>
						<Button
							size="sm"
							type="button"
							class="h-7 cursor-pointer"
							:disabled="isSaving"
							@click="applyChanges"
						>
							{{ isSaving ? 'Saving…' : 'Save changes' }}
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
	transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.18s ease;
}

.footer-slide-enter-from,
.footer-slide-leave-to {
	transform: translateY(16px);
	opacity: 0;
}
</style>
