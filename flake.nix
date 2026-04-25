{
  description = "Development environment for Grain";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        devtools = import ./nix/devtools.nix { inherit pkgs; };
        infra = import ./nix/infra.nix { inherit pkgs; };
        java = import ./backend/platform-api/nix/java.nix { inherit pkgs; };

        modules = [ devtools infra java ];

        allPackages = builtins.concatLists (map (m: m.packages) modules);
        allShellHooks = builtins.concatStringsSep "\n" (map (m: m.shellHook) modules);
      in
      {
        packages.brand-api-image = import ./backend/brand-api/nix/image.nix { inherit pkgs; };

        devShells.default = pkgs.mkShell {
          name = "grain-dev-env";
          packages = allPackages;
          shellHook = ''
            echo "Entering Grain development environment..."
          '' + allShellHooks;
        };
      }
    );
}
