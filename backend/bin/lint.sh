#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <module>" >&2
    exit 1
fi

module="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
backend_dir="$(cd "${script_dir}/.." && pwd)"

run_spotless_check() {
    local project_path="$1"
    local project_name="$2"

    echo "Running spotlessCheck for ${project_name}"
    (
        cd "${backend_dir}/${project_path}"
        ./gradlew --no-daemon spotlessCheck
    )
}

case "${module}" in
    platform)
        run_spotless_check "platform-api/platform-api-client" "platform-api-client"
        run_spotless_check "platform-api/platform-api-service" "platform-api-service"
        ;;
    platform-api-client)
        run_spotless_check "platform-api/platform-api-client" "platform-api-client"
        ;;
    platform-api-service)
        run_spotless_check "platform-api/platform-api-service" "platform-api-service"
        ;;
    *)
        echo "Unknown module: ${module}" >&2
        echo "Supported modules: platform, platform-api-client, platform-api-service" >&2
        exit 1
        ;;
esac
