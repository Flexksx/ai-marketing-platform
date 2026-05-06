{ pkgs, uv2nix, pyproject-nix, pyproject-build-systems }:
let
  python = pkgs.python314;

  workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ../..; };

  overlay = workspace.mkPyprojectOverlay {
    sourcePreference = "wheel";
  };

  # psycopg2-binary compiles against libpq — supply it at build time.
  pyprojectOverrides = _final: prev: {
    psycopg2-binary = prev.psycopg2-binary.overrideAttrs (old: {
      buildInputs       = (old.buildInputs       or [ ]) ++ [ pkgs.postgresql ];
      nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [ pkgs.postgresql ];
    });
  };

  pythonSet =
    (pkgs.callPackage pyproject-nix.build.packages {
      inherit python;
    }).overrideScope (
      pkgs.lib.composeManyExtensions [
        pyproject-build-systems.overlays.default
        overlay
        pyprojectOverrides
      ]
    );
in
{
  inherit python pythonSet workspace;
  pythonEnv = pythonSet.mkVirtualEnv "vozai-backend-env" workspace.deps.default;
}
