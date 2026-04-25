{ pkgs }:
{
  packages = with pkgs; [
    postgresql
    postgresql.lib
    docker-compose
    podman-compose
    supabase-cli
    openssl
    pkg-config
    gcc
    gcc.cc.lib
    zlib
    prisma-engines
    ngrok
    google-cloud-sdk
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.openssl.out}/lib:${pkgs.zlib.out}/lib:${pkgs.gcc.cc.lib}/lib:${pkgs.postgresql.lib}/lib:$LD_LIBRARY_PATH"
  '';
}
