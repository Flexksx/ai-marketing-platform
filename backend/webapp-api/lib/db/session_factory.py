from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from lib.db.session_manager import get_session


class DbSessionFactory:
    def session(self) -> AbstractAsyncContextManager[AsyncSession]:
        return get_session()
