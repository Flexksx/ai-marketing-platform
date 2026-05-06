{
  description = "Development environment for Vozai - TypeScript frontend and Python backend";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        moduleArgs = { inherit pkgs uv2nix pyproject-nix pyproject-build-systems; };

        nixLib     = import ./nix/lib.nix     { lib = pkgs.lib; };
        infraEnv   = import ./nix/infra.nix   moduleArgs;
        webEnv     = import ./apps/web/nix/web.nix    moduleArgs;
        backendEnv = import ./backend/nix     moduleArgs;

        merged = nixLib.mergeDevEnvs [ infraEnv webEnv backendEnv ];
      in
      {
        devShells.default = pkgs.mkShell {
          name = "vozai-fullstack-env";
          inherit (merged) packages shellHook;
        };

        packages.default = backendEnv.pythonEnv;
      }
    );
}
