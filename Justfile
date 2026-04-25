format module:
    ./backend/bin/format.sh {{module}}

format-nix:
    alejandra .

lint module:
    ./backend/bin/lint.sh {{module}}
