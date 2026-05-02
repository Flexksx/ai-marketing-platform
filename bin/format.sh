#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <target>" >&2
    exit 1
fi

target="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

# Ruff resolves shared rules via `[tool.ruff] extend = \"../ruff.toml\"` in each package's pyproject.toml.
backend_python_projects=(
    "${repo_root}/backend/webapp-api"
    "${repo_root}/backend/scraper-api"
    "${repo_root}/backend/webapp-api-contract"
    "${repo_root}/backend/scraper-api-contract"
)

format_python_package() {
    local proj_dir="$1"
    uv run --directory "${proj_dir}" ruff check --fix . || true
    uv run --directory "${proj_dir}" ruff format .
    uv run --directory "${proj_dir}" ty check --fix . || true
}

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
        for proj_dir in "${backend_python_projects[@]}"; do
            format_python_package "${proj_dir}"
        done
        ;;
    *)
        echo "Unknown format target: ${target}" >&2
        echo "Supported targets: all, nix, spa, api" >&2
        exit 1
        ;;
esac
