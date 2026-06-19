from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id) -> Optional[User]:
        q = select(User).where(User.id == user_id)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        q = select(User).where(User.email == email)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user
