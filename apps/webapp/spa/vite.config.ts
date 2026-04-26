import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";
import { defineConfig, loadEnv } from "vite";

const projectRoot = path.resolve(fileURLToPath(new URL(".", import.meta.url)));

const apiPathPrefixes = [
	"/actuator",
	"/v3",
	"/auth",
	"/users",
	"/brands",
	"/swagger-ui",
] as const;

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), "");
	const devApiProxyTarget = env.VITE_DEV_API_PROXY_TARGET || "http://127.0.0.1:8080";
	const devProxy: Record<string, { target: string; changeOrigin: true }> = {};
	for (const p of apiPathPrefixes) {
		devProxy[p] = { target: devApiProxyTarget, changeOrigin: true };
	}
	return {
		plugins: [vue(), tailwindcss()],
		server: {
			host: "0.0.0.0",
			port: 5173,
			proxy: devProxy,
			watch: {
				usePolling: true,
			},
			hmr: {
				host: "localhost",
				port: 5173,
			},
		},
		resolve: {
			alias: {
				"@": path.join(projectRoot, "src"),
			},
		},
	};
});
