format module:
    ./bin/format.sh {{module}}

lint module:
    ./backend/bin/lint.sh {{module}}

dev action target *flags:
    ./bin/dev.sh {{flags}} {{action}} {{target}}
