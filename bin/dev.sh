#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 [-c] <up|down> <platform|webapp|all>" >&2
    echo "  -c  Clean build (--build --force-recreate)" >&2
    exit 1
}

clean_build=false
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

compose_file="${repo_root}/backend/docker-compose.dev.yml"

platform_services=(postgres backend)
webapp_services=(spa)
all_services=()  # empty = all services in the file

target_services=()
case "${target}" in
    platform) target_services=("${platform_services[@]}") ;;
    webapp)   target_services=("${webapp_services[@]}") ;;
    all)      target_services=("${all_services[@]}") ;;
    *)
        echo "Unknown target: ${target}" >&2
        echo "Supported targets: platform, webapp, all" >&2
        exit 1
        ;;
esac

case "${action}" in
    up)
        up_flags=(-d)
        if [[ "${clean_build}" == true ]]; then
            up_flags+=(--build --force-recreate)
        fi
        docker compose --project-directory "${repo_root}" -f "${compose_file}" up "${up_flags[@]}" "${target_services[@]}"
        ;;
    down)
        docker compose --project-directory "${repo_root}" -f "${compose_file}" down "${target_services[@]}"
        ;;
    *)
        echo "Unknown action: ${action}" >&2
        echo "Supported actions: up, down" >&2
        exit 1
        ;;
esac
