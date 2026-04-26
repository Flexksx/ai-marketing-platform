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
        "${BASH_SOURCE[0]}" platform
        "${BASH_SOURCE[0]}" platform-api-client
        "${BASH_SOURCE[0]}" platform-api-service
        "${BASH_SOURCE[0]}" spa
        ;;
    nix)
        (
            cd "${repo_root}"
            alejandra .
        )
        ;;
    platform|platform-api-client|platform-api-service)
        "${repo_root}/backend/bin/format.sh" "${target}"
        ;;
    spa)
        (
            cd "${repo_root}/apps/webapp/spa"
            npm run format
        )
        ;;
    *)
        echo "Unknown format target: ${target}" >&2
        echo "Supported targets: all, nix, platform, platform-api-client, platform-api-service, spa" >&2
        exit 1
        ;;
esac
