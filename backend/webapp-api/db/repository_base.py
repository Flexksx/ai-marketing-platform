from sqlalchemy.ext.asyncio import AsyncSession


class TransactionAwareMixin:
    def __init__(self, db: AsyncSession, auto_commit: bool = True):
        self.db = db
        self.auto_commit = auto_commit

    async def _commit_if_needed(self) -> None:
        if self.auto_commit:
            await self.db.commit()

    async def _refresh_if_needed(self, instance) -> None:
        if self.auto_commit:
            await self.db.refresh(instance)

