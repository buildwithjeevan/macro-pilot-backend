from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.api.v1.auth_router import router as auth_router
from src.core.database.health import check_database_connection
from src.core.responses import register_exception_handlers, success_response, error_response


def create_app() -> FastAPI:
    app = FastAPI(title="MacroPilot API", version="0.1.0")
    register_exception_handlers(app)
    app.include_router(auth_router)

    @app.get("/healthz")
    async def health():
        """Liveness check: confirms the API process is running."""
        return success_response(
            data={"alive": True},
            message="Service is healthy",
        )

    @app.get("/healthz/db")
    async def health_db():
        """Readiness check: confirms the API can reach the database."""
        try:
            await check_database_connection()
        except Exception as exc:
            body = error_response(
                message="Database is disconnected",
                code=status.HTTP_503_SERVICE_UNAVAILABLE,
                data={"database": "disconnected", "detail": str(exc)},
            )
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=body.model_dump(mode="json"),
            )

        return success_response(
            data={"database": "connected"},
            message="Database is connected",
        )

    return app


app = create_app()
