-- Sets passwords for internal Supabase roles from POSTGRES_PASSWORD.
-- Must run after base image migrations (see supabase/postgres docker layout).
\set pgpass `echo "$POSTGRES_PASSWORD"`

ALTER USER authenticator WITH PASSWORD :'pgpass';
ALTER USER pgbouncer WITH PASSWORD :'pgpass';
ALTER USER supabase_auth_admin WITH PASSWORD :'pgpass';
-- supabase_functions_admin: omitted — not present on older supabase/postgres images (e.g. 15.8.1.060).
ALTER USER supabase_storage_admin WITH PASSWORD :'pgpass';
