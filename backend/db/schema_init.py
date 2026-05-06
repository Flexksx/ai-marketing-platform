import logging

from sqlalchemy import inspect, text

from db.database import Base, engine

logger = logging.getLogger(__name__)


async def ensure_schema(environment: str = "development") -> None:
    """
    Verify the DB schema matches the ORM models and create any missing tables.

    Dev mode: drops and recreates all public-schema tables if any expected
              column is absent. Handles legacy tables via CASCADE.
    Production mode: raises on mismatch — never auto-drops data.
    """
    async with engine.begin() as conn:
        mismatched = await conn.run_sync(_find_mismatched_tables)

    if mismatched:
        tables = ", ".join(mismatched)
        if environment != "production":
            logger.warning(
                "Schema mismatch in tables [%s] — resetting all public-schema "
                "tables and recreating from ORM models. All app data will be lost.",
                tables,
            )
            async with engine.begin() as conn:
                await conn.execute(text(_drop_all_public_tables_sql()))
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Schema reset complete.")
        else:
            raise RuntimeError(
                f"Schema mismatch detected in tables [{tables}]. "
                "Apply the required migrations before starting the service."
            )
    else:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Schema verified — all tables present and columns match.")


def _drop_all_public_tables_sql() -> str:
    return """
        DO $$
        DECLARE r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
    """


def _find_mismatched_tables(sync_conn) -> list[str]:
    inspector = inspect(sync_conn)
    existing_tables = set(inspector.get_table_names())
    mismatched = []

    for table_name, table in Base.metadata.tables.items():
        if table_name not in existing_tables:
            continue  # Missing tables are handled by create_all

        actual_columns = {col["name"] for col in inspector.get_columns(table_name)}
        expected_columns = {col.name for col in table.columns}

        if not expected_columns.issubset(actual_columns):
            missing = expected_columns - actual_columns
            logger.debug("Table %s is missing columns: %s", table_name, missing)
            mismatched.append(table_name)

    return mismatched
