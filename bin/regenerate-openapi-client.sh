#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
retries="${OPENAPI_FETCH_RETRIES:-30}"
delay_seconds="${OPENAPI_FETCH_DELAY_SECONDS:-2}"

attempt=1
while true; do
    if (cd "${repo_root}" && pnpm --filter @ai-marketing-platform/platform-api-client fetch-spec); then
        break
    fi

    if [[ "${attempt}" -ge "${retries}" ]]; then
        echo "Unable to fetch OpenAPI spec after ${retries} attempts from ${PLATFORM_API_OPENAPI_URL:-http://localhost:8080/v3/api-docs}" >&2
        exit 1
    fi

    echo "OpenAPI spec endpoint unavailable (attempt ${attempt}/${retries}), retrying in ${delay_seconds}s..." >&2
    attempt=$((attempt + 1))
    sleep "${delay_seconds}"
done

(cd "${repo_root}" && pnpm --filter @ai-marketing-platform/platform-api-client generate)
