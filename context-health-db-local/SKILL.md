---
name: context-health-db-local
description: Connect to the Context Health database locally (read/write) using DB_DIRECT_ENDPOINT and .env; includes psql, psycopg, and SQLAlchemy setup.
metadata:
  short-description: Connect to Context Health DB locally
---

# Context Health DB Local Access

Use this skill when you need to connect to the Context Health database from a local machine for queries, seeds, or debugging.

## Quick start (recommended)

1) `cd Backend`
2) Ensure `.env` has:
   - `DB_DIRECT_ENDPOINT`
   - `DB_NAME`
   - `DB_USERNAME`
   - `DB_PASSWORD`

If missing, run `make gen-env` to regenerate from Terraform outputs.

## Fast query template

Use the existing helper:
`Backend/scripts/ai_helper_templates/read_from_db.py`

Edit the `query(conn)` function and run:
```
python scripts/ai_helper_templates/read_from_db.py
```

## SQLAlchemy (direct connection)

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = (
    f"postgresql+pg8000://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_DIRECT_ENDPOINT']}/{os.environ['DB_NAME']}"
)
engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
```

## psql (direct)

```
PGPASSWORD="$DB_PASSWORD" psql \
  "host=$DB_DIRECT_ENDPOINT dbname=$DB_NAME user=$DB_USERNAME sslmode=require"
```

## Notes / gotchas

- Keep `.env` lines as `KEY=value` (no spaces) so `python-dotenv` loads them cleanly.
- If connection fails, confirm `DB_DIRECT_ENDPOINT` is reachable and credentials are current.
- When SSM is open, local commands that still try the private RDS hostname need a localhost override.
  For Alembic from `Backend/`, use:
  `DB_DIRECT_ENDPOINT=127.0.0.1 DB_PORT=5432 alembic current`
  and the same prefix for `alembic upgrade head` / `alembic check`.
  Use the overridden local port if SSM was started with `SSM_LOCAL_PORT=...`.
