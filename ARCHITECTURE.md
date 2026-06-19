MacroPilot Backend Architecture (Phase 1)

This document summarizes the architecture, module boundaries, folder layout, and decisions made for Phase 1.

See README for next steps.

Key decisions:
- Clean Architecture (onion): API -> Services -> Domain -> Infrastructure
- Async-first stack: FastAPI + SQLAlchemy Async + asyncpg
- JWT + refresh token rotation for auth
- Centralized config via Pydantic `Settings`
- Structured logging with request middleware
- Repositories + services for data access and business rules

Phase 1 created scaffold and config stubs. Next: implement SQLAlchemy async setup and Alembic wiring (Phase 2).
