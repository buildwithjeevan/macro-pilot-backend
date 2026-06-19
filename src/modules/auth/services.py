from typing import Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.repositories import UserRepository
from src.modules.users.models import User
from src.core.security.hash import hash_password, verify_password
from src.core.security.jwt import create_access_token
from src.core.security.tokens import generate_refresh_token, hash_token, refresh_token_expiry
from src.modules.auth.models import RefreshToken
from src.modules.auth.repositories import RefreshTokenRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)

    async def signup(self, email: str, password: str) -> User:
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        user = User(email=email, password_hash=hash_password(password))
        await self.user_repo.create(user)
        await self.session.commit()
        return user

    async def login(self, email: str, password: str) -> Optional[dict]:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        access_token = create_access_token(subject=str(user.id))

        # create refresh token record
        raw_refresh = generate_refresh_token()
        token_hash = hash_token(raw_refresh)
        expires_at = refresh_token_expiry()
        refresh = RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
        refresh_repo = RefreshTokenRepository(self.session)
        await refresh_repo.create(refresh)
        await self.session.commit()

        return {"access_token": access_token, "refresh_token": raw_refresh}

    async def refresh(self, provided_token: str) -> Optional[dict]:
        token_hash = hash_token(provided_token)
        refresh_repo = RefreshTokenRepository(self.session)
        record = await refresh_repo.get_by_hash(token_hash)
        if not record or record.revoked:
            return None
        if record.expires_at < datetime.utcnow():
            return None

        # rotate: revoke old and create new
        await refresh_repo.revoke(record)
        raw_refresh = generate_refresh_token()
        new_hash = hash_token(raw_refresh)
        expires_at = refresh_token_expiry()
        new_record = RefreshToken(user_id=record.user_id, token_hash=new_hash, expires_at=expires_at)
        await refresh_repo.create(new_record)
        await self.session.commit()

        new_access = create_access_token(subject=str(record.user_id))
        return {"access_token": new_access, "refresh_token": raw_refresh}
