import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/",
			redirect: "/calendar",
		},
		{
			path: "/calendar",
			name: "calendar",
			component: () => import("@/views/CalendarPage.vue"),
		},
		{
			path: "/brands",
			name: "brands",
			component: () => import("@/views/BrandsPage.vue"),
		},
		{
			path: "/brands/:brandId/settings",
			name: "brand-settings",
			component: () => import("@/views/BrandSettingsPage.vue"),
		},
	],
});
