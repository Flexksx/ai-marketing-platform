from db.session_factory import DbSessionFactory


def get_db_session_factory() -> DbSessionFactory:
    return DbSessionFactory()
