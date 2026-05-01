mod openapi

format module="all":
    ./bin/format.sh {{module}}

dev action target *flags:
    ./bin/dev.sh {{flags}} {{action}} {{target}}
