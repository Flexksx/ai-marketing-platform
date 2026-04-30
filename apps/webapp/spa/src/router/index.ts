import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/",
			redirect: "/brands",
		},
		{
			path: "/brands",
			name: "brands",
			component: () => import("@/views/BrandsPage.vue"),
		},
		{
			path: "/brands/:brandId",
			redirect: (to) => `/brands/${to.params.brandId}/settings`,
		},
		{
			path: "/brands/:brandId/settings",
			name: "brand-settings",
			component: () => import("@/views/BrandSettingsPage.vue"),
		},
		{
			path: "/brands/:brandId/calendar",
			name: "brand-calendar",
			component: () => import("@/views/CalendarPage.vue"),
		},
	],
});
