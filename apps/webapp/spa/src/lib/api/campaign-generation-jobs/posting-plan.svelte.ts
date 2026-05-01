import { SvelteMap } from 'svelte/reactivity';
import type { PostingPlanItemModification } from './CampaignGenerationJob';
import type { CampaignContentPlanItem } from './CampaignGenerationJobResult';

export class PostingPlanStore {
	#originalItems = $state<CampaignContentPlanItem[]>([]);
	#modifications = new SvelteMap<string, PostingPlanItemModification>();

	initialize(items: CampaignContentPlanItem[]) {
		this.#originalItems = items;
	}

	updateItem(id: string, updates: Partial<CampaignContentPlanItem>) {
		const existingMod = this.#modifications.get(id) || { item_id: id };

		if (updates.caption !== undefined) existingMod.caption = updates.caption;
		if (updates.scheduledAt !== undefined) existingMod.scheduled_at = updates.scheduledAt;
		if (updates.imageUrls !== undefined && updates.imageUrls.length > 0) {
			existingMod.image_url = updates.imageUrls[0];
			existingMod.available_image_urls = updates.imageUrls;
		}

		this.#modifications.set(id, existingMod);
	}

	get items() {
		return this.#originalItems.map((item) => {
			const mod = this.#modifications.get(item.id);
			if (!mod) return item;

			return {
				...item,
				caption: mod.caption !== undefined ? mod.caption : item.caption,
				scheduledAt: mod.scheduled_at !== undefined ? mod.scheduled_at : item.scheduledAt,
				imageUrls: mod.available_image_urls ? mod.available_image_urls : item.imageUrls
			};
		});
	}

	get modifications() {
		return Array.from(this.#modifications.values());
	}

	isModified(id: string) {
		return this.#modifications.has(id);
	}

	reset() {
		this.#modifications.clear();
	}
}

export const postingPlanStore = new PostingPlanStore();
