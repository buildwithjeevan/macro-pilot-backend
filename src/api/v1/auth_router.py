from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.schemas import (
    SignupRequest,
    LoginRequest,
    RefreshRequest,
    TokenResponse,
    MeResponse,
)
from src.core.database.session import get_session
from src.core.responses import BaseResponse, success_response
from src.modules.auth.services import AuthService
from src.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=BaseResponse[TokenResponse],
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    payload: SignupRequest,
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(session)
    try:
        await service.signup(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    tokens = await service.login(payload.email, payload.password)
    return success_response(
        data={
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
        },
        message="User registered successfully",
        code=status.HTTP_201_CREATED,
    )


@router.post("/login", response_model=BaseResponse[TokenResponse])
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    service = AuthService(session)
    tokens = await service.login(payload.email, payload.password)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return success_response(
        data={
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
        },
        message="Login successful",
    )


@router.post("/refresh", response_model=BaseResponse[TokenResponse])
async def refresh(payload: RefreshRequest, session: AsyncSession = Depends(get_session)):
    service = AuthService(session)
    tokens = await service.refresh(payload.refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return success_response(
        data={
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
        },
        message="Token refreshed successfully",
    )


@router.post("/logout", response_model=BaseResponse[None])
async def logout(payload: RefreshRequest, session: AsyncSession = Depends(get_session)):
    from src.modules.auth.repositories import RefreshTokenRepository
    from src.core.security.tokens import hash_token

    token_hash = hash_token(payload.refresh_token)
    repo = RefreshTokenRepository(session)
    record = await repo.get_by_hash(token_hash)
    if record:
        await repo.revoke(record)
        await session.commit()
    return success_response(data=None, message="Logged out successfully")


@router.get("/me", response_model=BaseResponse[MeResponse])
async def me(current_user=Depends(get_current_user)):
    return success_response(
        data={
            "id": str(current_user.id),
            "email": current_user.email,
            "is_active": current_user.is_active,
        },
        message="Current user retrieved successfully",
    )
