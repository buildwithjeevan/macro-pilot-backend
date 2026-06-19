from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.modules.auth.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        q = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        res = await self.session.execute(q)
        return res.scalars().first()

    async def revoke(self, token: RefreshToken) -> None:
        token.revoked = True
        self.session.add(token)
        await self.session.flush()

    async def revoke_all_for_user(self, user_id) -> None:
        q = update(RefreshToken).where(RefreshToken.user_id == user_id).values(revoked=True)
        await self.session.execute(q)
        await self.session.flush()
