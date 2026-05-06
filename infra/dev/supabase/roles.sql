-- Set passwords for Supabase internal service roles.
-- The supabase/postgres image creates these roles but does not set passwords by default.
-- This script runs on first container init via docker-entrypoint-initdb.d.
-- POSTGRES_PASSWORD is available in the environment at init time.

\set pgpassword `echo "$POSTGRES_PASSWORD"`

ALTER USER supabase_admin         WITH PASSWORD :'pgpassword';
ALTER USER authenticator          WITH PASSWORD :'pgpassword';
ALTER USER supabase_auth_admin    WITH PASSWORD :'pgpassword';
ALTER USER supabase_storage_admin WITH PASSWORD :'pgpassword';
