#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

(cd "${repo_root}" && ./bin/regenerate-openapi-client.sh)

(
    cd "${repo_root}" &&
        pnpm exec chokidar \
            "backend/platform-api/platform-api-client/src/main/**/*.java" \
            "backend/platform-api/platform-api-service/src/main/**/*.java" \
            "backend/platform-api/platform-api-service/src/main/resources/**/*.yml" \
            "backend/platform-api/platform-api-service/src/main/resources/**/*.yaml" \
            "backend/platform-api/platform-api-service/src/main/resources/**/*.properties" \
            "backend/platform-api/platform-api-client/src/main/resources/**/*.yml" \
            "backend/platform-api/platform-api-client/src/main/resources/**/*.yaml" \
            "backend/platform-api/platform-api-client/src/main/resources/**/*.properties" \
            -i "**/build/**" \
            --debounce 2000 \
            -c "sleep 2 && ./bin/regenerate-openapi-client.sh"
)
