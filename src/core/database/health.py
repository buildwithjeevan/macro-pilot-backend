from sqlalchemy import text

from src.core.database.engine import get_engine


async def check_database_connection() -> None:
    """Run a lightweight query to verify the database is reachable."""
    async with get_engine().connect() as conn:
        await conn.execute(text("SELECT 1"))
