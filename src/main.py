from fastapi import FastAPI
from src.api.v1.auth_router import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="MacroPilot API", version="0.1.0")
    app.include_router(auth_router)

    @app.get("/healthz")
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
