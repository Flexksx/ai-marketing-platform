{ pkgs, ... }:
{
  packages = with pkgs; [
    docker-compose # local Supabase stack (see docker-compose.yml)
    supabase-cli # manage local Supabase instance, migrations, edge functions
    google-cloud-sdk # deploy to GCP, access Cloud Run / Storage / Secret Manager
    wrangler # Cloudflare Workers — edge functions and KV
    prisma-engines # Prisma query engine binaries required by the Prisma CLI
    ngrok # expose local services over a public tunnel (webhooks, OAuth callbacks)
    just
  ];

  shellHook = ''
    echo "  Infra: docker-compose, supabase-cli, gcloud, wrangler, ngrok"
  '';
}
