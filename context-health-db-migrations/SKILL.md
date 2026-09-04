---
name: context-health-db-migrations
description: Context Health DB migration workflow. Update SQLAlchemy models in Backend/core/models, run alembic --autogenerate, then edit the version file so DB matches models exactly. Prevent drift.
---

# Context Health DB migrations

## Scope
- Use for any schema change: tables, columns, indexes, enums, constraints.
- Models are source of truth. DB must match models; never reverse.

## Workflow
1) Update SQLAlchemy models in `Backend/core/models/` only.
2) Ensure DB at head.
   - `cd /Users/akramreshad/src/Context_Health/Backend`
   - `source venv/bin/activate`
   - `alembic upgrade head`
   - If SSM is open and the direct RDS hostname still fails, force Alembic through the local tunnel: `DB_DIRECT_ENDPOINT=127.0.0.1 DB_PORT=5432 alembic upgrade head`. Use the active `SSM_LOCAL_PORT` value if it is not `5432`.
3) Autogenerate migration.
   - `alembic revision --autogenerate -m "<msg>"`
4) Edit the new version file.
   - Keep schema, types, nullability, indexes, FKs aligned to models.
   - Do not add DB defaults unless models use `server_default`.
   - Enums: name + schema must match model enums; add values only if models updated.
   - Remove noise that does not reflect model changes.
5) Re-run `alembic upgrade head` to verify.
6) If enums already exist from a failed run, drop them explicitly or wrap creation in `if not exists` checks. Do not change models to match DB.
