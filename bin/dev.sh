#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 [-c] [--prod] <up|down> <back|ui>" >&2
    echo "  -c      Clean build for docker targets (--build --force-recreate)" >&2
    echo "  --prod  (ui only) connect to production backend; default is local" >&2
    exit 1
}

clean_build=false
prod_mode=false

# Parse long options before getopts
args=()
for arg in "$@"; do
    case "${arg}" in
        --prod) prod_mode=true ;;
        *)      args+=("${arg}") ;;
    esac
done
set -- "${args[@]}"

while getopts "c" opt; do
    case "${opt}" in
        c) clean_build=true ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))

if [[ $# -ne 2 ]]; then
    usage
fi

action="$1"
target="$2"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

case "${target}" in
    back)
        compose_file="${repo_root}/docker-compose.dev.yml"
        case "${action}" in
            up)
                up_flags=(-d)
                if [[ "${clean_build}" == true ]]; then
                    up_flags+=(--build --force-recreate)
                fi
                docker compose --project-directory "${repo_root}" -f "${compose_file}" up "${up_flags[@]}"
                ;;
            down)
                docker compose --project-directory "${repo_root}" -f "${compose_file}" down
                ;;
            *)
                echo "Unknown action: ${action}" >&2
                echo "Supported actions: up, down" >&2
                exit 1
                ;;
        esac
        ;;
    ui)
        case "${action}" in
            up)
                if [[ "${prod_mode}" == true ]]; then
                    pnpm --filter spa run dev:prod
                else
                    pnpm --filter spa run dev:local
                fi
                ;;
            down)
                echo "ui target runs in the foreground; use Ctrl+C to stop it." >&2
                ;;
            *)
                echo "Unknown action: ${action}" >&2
                echo "Supported actions: up, down" >&2
                exit 1
                ;;
        esac
        ;;
    *)
        echo "Unknown target: ${target}" >&2
        echo "Supported targets: back, ui" >&2
        exit 1
        ;;
esac
