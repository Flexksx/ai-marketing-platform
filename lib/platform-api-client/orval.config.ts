import { defineConfig } from 'orval';

export default defineConfig({
  platformApi: {
    input: {
      target: './openapi.json',
    },
    output: {
      mode: 'tags',
      target: './src/generated/api.ts',
      client: 'axios',
      httpClient:"axios",
      clean: true,
      override: {
        mutator: {
          path: './src/mutator.ts',
          name: 'customInstance',
        },
      },
    },
  },
});
