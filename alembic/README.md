Alembic Migrations

- Configure `DATABASE_URL` in your environment (or .env) before running migrations.
- Generate migration:

```bash
alembic revision --autogenerate -m "create initial tables"
```

- Apply migrations:

```bash
alembic upgrade head
```

Notes:
- `env.py` loads `src.core.database.Base.metadata` for autogeneration.
- Ensure `src` package is importable (run commands from project root).
