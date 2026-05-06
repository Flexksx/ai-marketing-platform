{ pkgs }:
let
  # Every shared library the Chromium sandbox and renderer need at runtime.
  chromeRuntimeLibs = with pkgs; [
    glib nss nspr atk at-spi2-atk
    cups.lib expat libxkbcommon libdrm
    xorg.libX11 xorg.libXcomposite xorg.libXdamage
    xorg.libXext xorg.libXfixes xorg.libXrandr
    mesa cairo pango udev alsa-lib dbus.lib
  ];

  # Browser binaries pre-patched for NixOS (correct interpreter paths, rpath).
  nixosBrowsers = pkgs.playwright-driver.browsers;
in
{
  packages = with pkgs; [
    playwright
    nixosBrowsers
    chromium
  ] ++ chromeRuntimeLibs;

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath chromeRuntimeLibs}:$LD_LIBRARY_PATH"
    export PLAYWRIGHT_BROWSERS_PATH=${nixosBrowsers}
    export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
    export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
  '';
}
