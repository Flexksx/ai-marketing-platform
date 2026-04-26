import { QueryClient, VueQueryPlugin } from "@tanstack/vue-query";
import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			staleTime: 60_000,
			gcTime: 5 * 60_000,
			retry: 1,
			refetchOnWindowFocus: true,
		},
		mutations: {
			retry: 0,
		},
	},
});

const app = createApp(App);
app.use(VueQueryPlugin, { queryClient });
app.mount("#app");
