{pkgs, ...}: {
  packages = with pkgs; [
    typescript
    pnpm
  ];
  shellHook = ''
    export PATH=$PATH:${pkgs.typescript}/bin
    export PATH=$PATH:${pkgs.pnpm}/bin
  '';
}
