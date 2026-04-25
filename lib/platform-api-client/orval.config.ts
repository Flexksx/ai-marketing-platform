import { defineConfig } from 'orval';

export default defineConfig({
  platformApi: {
    input: {
      target: './openapi.json',
    },
    output: {
      mode: 'tags-split',
      target: './src/generated',
      schemas: './src/generated/models',
      client: 'axios',
      clean: true,
      override: {
        mutator: {
          path: './src/mutator.ts',
          name: 'platformApiInstance',
        },
      },
    },
  },
});
