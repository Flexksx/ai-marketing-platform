{
  description = "Development environment for Voz AI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        devtools = import ./nix/devtools.nix {inherit pkgs;};
        infra = import ./nix/infra.nix {inherit pkgs;};
        typescript = import ./apps/webapp/nix/typescript.nix {inherit pkgs;};
        python = import ./backend/webapp-api/nix/python.nix {inherit pkgs;};

        modules = [devtools infra typescript python];

        allPackages = builtins.concatLists (map (m: m.packages) modules);
        allShellHooks = builtins.concatStringsSep "\n" (map (m: m.shellHook) modules);
      in {
        devShells.default = pkgs.mkShell {
          name = "vozai-dev-env";
          packages = allPackages;
          shellHook =
            ''
              echo "Entering Voz AI development environment..."
              REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

              ln -sfn "${pkgs.nodejs_24}" "$REPO_ROOT/.nix-nodejs"
              ln -sfn "${pkgs.pnpm}" "$REPO_ROOT/.nix-pnpm"
            ''
            + allShellHooks;
        };
      }
    );
}
