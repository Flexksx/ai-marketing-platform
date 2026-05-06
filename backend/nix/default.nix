{ pkgs, uv2nix, pyproject-nix, pyproject-build-systems, ... }:
let
  pythonModule  = import ./python.nix    { inherit pkgs uv2nix pyproject-nix pyproject-build-systems; };
  playwrightEnv = import ./playwright.nix { inherit pkgs; };

  # C/C++ toolchain + system libs needed to compile Python extensions
  # (psycopg2, cryptography, etc.) and resolve them at runtime.
  nativeBuildLibs = with pkgs; [
    openssl pkg-config
    gcc gcc.cc.lib
    zlib
    postgresql postgresql.lib
  ];
in
{
  packages =
    [ pythonModule.python pkgs.uv ]
    ++ playwrightEnv.packages
    ++ nativeBuildLibs;

  shellHook = ''
    echo "  Backend: Python ${pythonModule.python.version}, uv"

    export LD_LIBRARY_PATH="${pkgs.openssl.out}/lib:${pkgs.zlib.out}/lib:${pkgs.gcc.cc.lib}/lib:${pkgs.postgresql.lib}/lib:$LD_LIBRARY_PATH"

    ${playwrightEnv.shellHook}

    if [ -f "pyproject.toml" ]; then
      echo "  Syncing Python dependencies with uv..."
      uv sync
      echo "  Python backend environment ready"
    fi
  '';

  inherit (pythonModule) pythonEnv;
}
