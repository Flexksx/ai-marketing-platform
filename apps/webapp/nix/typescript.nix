{pkgs, ...}: {
  packages = with pkgs; [
    typescript
    pnpm
  ];
}
