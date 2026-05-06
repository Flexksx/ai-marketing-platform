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
      self,
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
          config = {
            allowUnfree = true;
          };
        };

        python = pkgs.python314;

        workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "wheel";
        };

        pyprojectOverrides = final: prev: {
          psycopg2-binary = prev.psycopg2-binary.overrideAttrs (old: {
            buildInputs = (old.buildInputs or [ ]) ++ [ pkgs.postgresql ];
            nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [ pkgs.postgresql ];
          });
        };

        pythonSet =
          (pkgs.callPackage pyproject-nix.build.packages {
            inherit python;
          }).overrideScope
            (
              pkgs.lib.composeManyExtensions [
                pyproject-build-systems.overlays.default
                overlay
                pyprojectOverrides
              ]
            );

        # Browser dependencies for Playwright/crawl4ai
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

      in
      {
        devShells.default = pkgs.mkShell {
          name = "vozai-fullstack-env";

          packages =
            with pkgs;
            [
              # Node.js / TypeScript / Frontend
              nodejs_24
              corepack
              pnpm
              typescript-go
              nodePackages.typescript
              nodePackages.typescript-language-server
              nodePackages.eslint
              nodePackages.prettier

              # Python / Backend
              python
              uv

              # Database & Infrastructure
              postgresql
              postgresql.lib
              docker-compose

              # Supabase
              supabase-cli

              # Browser automation dependencies for crawl4ai/Playwright
              # Use playwright-driver.browsers for NixOS compatibility
              playwright
              playwright-driver.browsers
              # Include chromium for Playwright to use
              chromium

              # Build tools & libraries
              openssl
              pkg-config
              gcc
              gcc.cc.lib
              zlib
              wrangler
              prisma-engines
              ngrok

              # Google Cloud SDK
              google-cloud-sdk
            ]
            ++ browserDeps;

          shellHook = ''
            echo "🚀 Entering Vozai development environment..."
            echo "  Frontend: Node.js ${pkgs.nodejs_24.version}, pnpm"
            echo "  Backend: Python ${python.version}, uv"

            # Set library paths for both TypeScript and Python dependencies
            export LD_LIBRARY_PATH="${pkgs.openssl.out}/lib:${pkgs.zlib.out}/lib:${pkgs.gcc.cc.lib}/lib:${pkgs.postgresql.lib}/lib:$LD_LIBRARY_PATH"

            # Add Playwright/browser library paths using Nix's makeLibraryPath
            export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath browserDeps}:$LD_LIBRARY_PATH"

            # Configure Playwright for NixOS (following NixOS wiki recommendations)
            # See: https://nixos.wiki/wiki/Playwright
            export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
            export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
            export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true


            # Auto-sync uv dependencies for backend if needed
            if [ -f "pyproject.toml" ]; then
              echo "📦 Syncing Python backend dependencies with uv..."
              uv sync
              echo "✓ Python backend environment is ready"
            fi

            echo "✨ Ready! Use 'uv run <command>' for Python (from root) or 'cd apps/web' for TypeScript"
          '';
        };

        packages = {
          default = pythonSet.mkVirtualEnv "vozai-backend-env" workspace.deps.default;
        };
      }
    );
}
