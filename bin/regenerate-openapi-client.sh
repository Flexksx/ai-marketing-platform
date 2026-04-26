#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

PLATFORM_API_URL="${PLATFORM_API_OPENAPI_URL:-http://localhost:8080/v3/api-docs}"

# Try to fetch from running server first (fastest for dev)
echo "Checking if platform-api is running at ${PLATFORM_API_URL}..."
if curl -sf "${PLATFORM_API_URL}" > /dev/null 2>&1; then
    echo "Server is up, fetching OpenAPI spec..."
    (cd "${repo_root}" && pnpm --filter @ai-marketing-platform/platform-api-client fetch-spec)
else
    echo "Server is down, trying to generate via Gradle (this might take a while)..."
    if (cd "${repo_root}/backend/platform-api/platform-api-service" && ./gradlew generateOpenApiDocs); then
        echo "OpenAPI spec generated successfully from service."
    elif (cd "${repo_root}/backend/platform-api/platform-api-client" && ./gradlew generateOpenApiDocs); then
        echo "OpenAPI spec generated successfully from client."
    else
        echo "Error: Could not generate OpenAPI spec. Is the server running?" >&2
        exit 1
    fi
fi

echo "Generating TypeScript client..."
(cd "${repo_root}" && pnpm --filter @ai-marketing-platform/platform-api-client generate)

echo "Done!"
