Database architecture notes

- Use PostgreSQL as primary datastore.
- SQLAlchemy 2.0 (async) + asyncpg driver.
- Use UUID primary keys for public-facing IDs (consider BigInt for extreme scale).
- Each module defines its SQLAlchemy models under `modules/<feature>/models.py`.
- Central `Base` metadata will be exposed from `src.core.database` for Alembic autogeneration.
- Connection management:
  - Create single async engine at application startup.
  - Provide `async_session` (scoped) via FastAPI dependency injection.
- Migration strategy:
  - Use Alembic with `env.py` importing `src.core.database.Base.metadata`.
  - Autogenerate migrations and review before applying.
