{pkgs}: let
  browserDeps = with pkgs; [
    glib
    nss
    nspr
    atk
    at-spi2-atk
    cups.lib
    expat
    libxkbcommon
    libdrm
    xorg.libX11
    xorg.libXcomposite
    xorg.libXdamage
    xorg.libXext
    xorg.libXfixes
    xorg.libXrandr
    mesa
    cairo
    pango
    udev
    alsa-lib
    dbus.lib
  ];
in {
  packages =
    (with pkgs; [
      python314
      uv
      playwright
      playwright-driver.browsers
      chromium
    ])
    ++ browserDeps;

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath browserDeps}:$LD_LIBRARY_PATH"

    export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
    export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
    export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true

    if [ -f "$REPO_ROOT/backend/scraper-api/pyproject.toml" ]; then
      echo "Syncing scraper-api Python dependencies..."
      (cd "$REPO_ROOT/backend/scraper-api" && uv sync)
    fi
  '';
}
