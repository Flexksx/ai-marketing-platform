{ pkgs, ... }:
{
  packages = with pkgs; [
    # Runtime
    nodejs_24
    corepack
    pnpm

    # TypeScript toolchain
    typescript-go
    nodePackages.typescript
    nodePackages.typescript-language-server

    # Linting / formatting
    nodePackages.eslint
    nodePackages.prettier
  ];

  shellHook = ''
    echo "  Frontend: Node.js ${pkgs.nodejs_24.version}, pnpm ${pkgs.pnpm.version}"
  '';
}
