from fastapi import APIRouter, Depends, status, Response

from src.modules.auth.schemas import SignupRequest, LoginRequest, TokenResponse, MeResponse
from src.core.database.session import get_session
from src.modules.auth.services import AuthService
from src.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest, response: Response, session=Depends(get_session)):
    async with session:
        service = AuthService(session)
        user = await service.signup(payload.email, payload.password)
        tokens = await service.login(payload.email, payload.password)
        return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, response: Response, session=Depends(get_session)):
    async with session:
        service = AuthService(session)
        tokens = await service.login(payload.email, payload.password)
        if not tokens:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: dict, session=Depends(get_session)):
    # expects {"refresh_token": "..."}
    token = payload.get("refresh_token")
    if not token:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    async with session:
        service = AuthService(session)
        tokens = await service.refresh(token)
        if not tokens:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: dict, session=Depends(get_session)):
    # expects {"refresh_token": "..."}
    token = payload.get("refresh_token")
    if not token:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    async with session:
        # revoke the refresh token if present
        from src.modules.auth.repositories import RefreshTokenRepository
        from src.core.security.tokens import hash_token

        token_hash = hash_token(token)
        repo = RefreshTokenRepository(session)
        record = await repo.get_by_hash(token_hash)
        if record:
            await repo.revoke(record)
            await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=MeResponse)
async def me(current_user=Depends(get_current_user)):
    return {"id": str(current_user.id), "email": current_user.email, "is_active": current_user.is_active}
