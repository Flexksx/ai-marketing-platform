#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

backend_dir="${repo_root}/backend/webapp-api"
spa_dir="${repo_root}/apps/webapp/spa"
schema_file="${repo_root}/openapi.json"

echo "Exporting OpenAPI schema from FastAPI app..."
# DATABASE_URL is validated at import time but never used during schema export.
DATABASE_URL="postgresql://dummy:dummy@localhost:5432/dummy" \
DIRECT_URL="postgresql://dummy:dummy@localhost:5432/dummy" \
    "${backend_dir}/.venv/bin/python" -c "
import sys
sys.path.insert(0, '${backend_dir}')
from services.client_api.main import app
import json
json.dump(app.openapi(), open('${schema_file}', 'w'), indent=2)
"
echo "Schema written to ${schema_file}"

echo "Generating TypeScript client..."
OPENAPI_URL="${schema_file}" pnpm --dir "${spa_dir}" run generate:api

echo "Done."
