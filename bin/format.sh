#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <target>" >&2
    exit 1
fi

target="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

case "${target}" in
    all)
        "${BASH_SOURCE[0]}" nix
        "${BASH_SOURCE[0]}" spa
        "${BASH_SOURCE[0]}" api
        ;;
    nix)
        (cd "${repo_root}" && alejandra .)
        ;;
    spa)
        (cd "${repo_root}/apps/webapp/spa" && pnpm run format:write && pnpm run lint:write)
        ;;
    api)
        (cd "${repo_root}/backend/webapp-api" && \
            uv run ruff check --fix . || true; \
            uv run ruff format . ; \
            uv run ty check --fix . || true)
        ;;
    *)
        echo "Unknown format target: ${target}" >&2
        echo "Supported targets: all, nix, spa, api" >&2
        exit 1
        ;;
esac
