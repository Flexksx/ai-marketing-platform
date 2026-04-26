format module="all":
    ./bin/format.sh {{module}}

lint module:
    ./backend/bin/lint.sh {{module}}

dev action target *flags:
    ./bin/dev.sh {{flags}} {{action}} {{target}}

openapi action="gen":
    @case "{{action}}" in \
        gen) ./bin/regenerate-openapi-client.sh ;; \
        watch) ./bin/watch-openapi-client.sh ;; \
        *) echo "Usage: just openapi [gen|watch]" && exit 1 ;; \
    esac
