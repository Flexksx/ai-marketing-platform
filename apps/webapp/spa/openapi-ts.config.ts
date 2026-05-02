import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
	input: process.env.OPENAPI_URL ?? 'http://localhost:8000/openapi.json',
	output: {
		path: 'src/lib/api/generated',
		postProcess: []
	},
	plugins: [
		'@hey-api/typescript',
		{
			name: '@hey-api/sdk',
			operations: { strategy: 'single' }
		},
		'@hey-api/client-axios'
	]
});
