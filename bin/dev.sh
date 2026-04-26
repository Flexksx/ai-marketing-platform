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

backend_compose_file="${repo_root}/backend/docker-compose.dev.yml"
spa_dir="${repo_root}/apps/webapp/spa"

webapp_pid_file="${repo_root}/.webapp.pid"
openapi_pid_file="${repo_root}/.openapi-watcher.pid"

run_webapp_up() {
    cd "${spa_dir}" && pnpm dev &
    echo $! > "${webapp_pid_file}"
    echo "webapp started (pid $(cat "${webapp_pid_file}"))"
}

run_openapi_watcher_up() {
    "${repo_root}/bin/watch-openapi-client.sh" &
    echo $! > "${openapi_pid_file}"
    echo "openapi watcher started (pid $(cat "${openapi_pid_file}"))"
}

run_webapp_down() {
    if [[ -f "${webapp_pid_file}" ]]; then
        kill "$(cat "${webapp_pid_file}")" 2>/dev/null && echo "webapp stopped"
        rm -f "${webapp_pid_file}"
    else
        echo "webapp pid file not found; process may already be stopped" >&2
    fi
}

run_openapi_watcher_down() {
    if [[ -f "${openapi_pid_file}" ]]; then
        # kill the entire process group to make sure chokidar and children are dead
        pkill -P "$(cat "${openapi_pid_file}")" 2>/dev/null || true
        kill "$(cat "${openapi_pid_file}")" 2>/dev/null && echo "openapi watcher stopped"
        rm -f "${openapi_pid_file}"
    fi
}

case "${target}" in
    platform)
        compose_files=(-f "${backend_compose_file}")
        ;;
    webapp)
        case "${action}" in
            up) run_webapp_up ;;
            down) run_webapp_down ;;
            *) echo "Unknown action: ${action}" >&2; exit 1 ;;
        esac
        exit 0
        ;;
    all)
        compose_files=(-f "${backend_compose_file}")
        ;;
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
        docker compose --project-directory "${repo_root}" "${compose_files[@]}" up "${up_flags[@]}"
        run_openapi_watcher_up
        if [[ "${target}" == "all" ]]; then
            run_webapp_up
        fi
        ;;
    down)
        run_openapi_watcher_down
        run_webapp_down
        docker compose --project-directory "${repo_root}" "${compose_files[@]}" down
        ;;
    *)
        echo "Unknown action: ${action}" >&2
        echo "Supported actions: up, down" >&2
        exit 1
        ;;
esac
