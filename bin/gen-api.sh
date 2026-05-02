#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

backend_dir="${repo_root}/backend/webapp-api"
spa_dir="${repo_root}/apps/webapp/spa"
schema_file="${repo_root}/openapi.json"

echo "Exporting OpenAPI schema from FastAPI app..."
python_bin="${backend_dir}/.venv/bin/python"
if ! [[ -x "${python_bin}" ]]; then
	echo "error: missing venv interpreter at ${python_bin} (create the backend venv first)" >&2
	exit 1
fi
# DATABASE_URL is validated at import time but never used during schema export.
DATABASE_URL="postgresql://dummy:dummy@localhost:5432/dummy" \
DIRECT_URL="postgresql://dummy:dummy@localhost:5432/dummy" \
	"${python_bin}" -c "
import json
import sys
sys.path.insert(0, '${backend_dir}')
from src.main import app
with open('${schema_file}', 'w', encoding='utf-8') as f:
    json.dump(app.openapi(), f, indent=2)
"
echo "Schema written to ${schema_file}"

echo "Generating TypeScript client..."
OPENAPI_INPUT="${schema_file}" pnpm --dir "${spa_dir}" run generate:api

echo "Done."
