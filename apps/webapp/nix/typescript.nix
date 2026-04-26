{pkgs, ...}: {
  packages = with pkgs; [
    nodejs_24
    typescript
    pnpm
  ];
  shellHook = ''

  '';
}
