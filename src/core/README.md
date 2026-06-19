Core module responsibilities

- `config`: environment and app settings (pydantic Settings).
- `database`: DB engine, session factory, Base metadata.
- `logging`: structured logger configuration (structlog/loguru) and request logging middleware.
- `security`: password hashing, JWT utilities, token helpers.
- `exceptions`: centralized exception definitions.
- `responses`: common response builder used across the API.

These components are thin adapters used by feature modules; keep business logic inside `modules/` services.
