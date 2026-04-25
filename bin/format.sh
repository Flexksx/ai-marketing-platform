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
    nix)
        (
            cd "${repo_root}"
            alejandra .
        )
        ;;
    platform|platform-api-client|platform-api-service)
        "${repo_root}/backend/bin/format.sh" "${target}"
        ;;
    *)
        echo "Unknown format target: ${target}" >&2
        echo "Supported targets: nix, platform, platform-api-client, platform-api-service" >&2
        exit 1
        ;;
esac
