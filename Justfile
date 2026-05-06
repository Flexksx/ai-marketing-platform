# Vozai — development commands

# Usage: just dev [up|down|ui|back]
dev action:
    #!/usr/bin/env bash
    case "{{action}}" in
      up)   docker compose up -d ;;
      down) docker compose down ;;
      ui)   cd apps/web && pnpm dev:local ;;
      back) uv run serve-api ;;
      *)    echo "Unknown action: {{action}}. Use: up, down, ui, back" && exit 1 ;;
    esac

# Usage: just format [ui|back]
format action:
    #!/usr/bin/env bash
    case "{{action}}" in
      ui)   cd apps/web && pnpm format ;;
      back) uv run ruff format . ;;
      *)    echo "Unknown action: {{action}}. Use: ui, back" && exit 1 ;;
    esac
