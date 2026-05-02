# Export FastAPI OpenAPI schema (repo `openapi.json`) and regenerate the webapp client.
# Types use camelCase; JSON bodies remain snake_case (OpenAPI Generator typescript-fetch).
gen:
    ./bin/gen-api.sh

# Regenerate only the SPA TypeScript client from the committed `openapi.json` (no Python).
gen-client:
    OPENAPI_INPUT="{{ justfile_directory() }}/openapi.json" pnpm --dir "{{ justfile_directory() }}/apps/webapp/spa" run generate:api
