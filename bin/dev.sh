#c!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <up|down> <platform|webapp|all>" >&2
    exit 1
fi

action="$1"
target="$2"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

backend_compose_file="${repo_root}/backend/docker-compose.dev.yml"
webapp_compose_file="${repo_root}/docker-compose.dev.yml"

case "${target}" in
    platform)
        compose_files=(-f "${backend_compose_file}")
        ;;
    webapp)
        compose_files=(-f "${webapp_compose_file}")
        ;;
    all)
        compose_files=(-f "${backend_compose_file}" -f "${webapp_compose_file}")
        ;;
    *)
        echo "Unknown target: ${target}" >&2
        echo "Supported targets: platform, webapp, all" >&2
        exit 1
        ;;
esac

case "${action}" in
    up)
        docker compose --project-directory "${repo_root}" "${compose_files[@]}" up -d
        ;;
    down)
        docker compose --project-directory "${repo_root}" "${compose_files[@]}" down
        ;;
    *)
        echo "Unknown action: ${action}" >&2
        echo "Supported actions: up, down" >&2
        exit 1
        ;;
esac
