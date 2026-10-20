import json
import os
from pathlib import Path
import sqlite3
import time
import uuid


def database_path():
    return Path(os.environ.get("CODEX_HOOK_ACTIVITY_DB", Path.home() / ".codex/hooks.sqlite3"))


def connect():
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=10)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""CREATE TABLE IF NOT EXISTS hook_runs (
        id TEXT PRIMARY KEY, hook TEXT NOT NULL, started_at REAL NOT NULL,
        finished_at REAL, status TEXT NOT NULL, session_id TEXT, turn_id TEXT,
        cwd TEXT, transcript_path TEXT, details TEXT NOT NULL
    )""")
    db.commit()
    return db


class HookRun:
    def __init__(self, hook, client):
        self.id = uuid.uuid4().hex
        self.details = {"client": client}
        with connect() as db:
            db.execute("INSERT INTO hook_runs (id, hook, started_at, status, details) VALUES (?, ?, ?, ?, ?)",
                       (self.id, hook, time.time(), "running", json.dumps(self.details)))

    def event(self, event):
        with connect() as db:
            db.execute("UPDATE hook_runs SET session_id=?, turn_id=?, cwd=?, transcript_path=? WHERE id=?",
                       (event.get("session_id"), event.get("turn_id"), event.get("cwd"), event.get("transcript_path"), self.id))

    def update(self, **details):
        self.details.update(details)
        with connect() as db:
            db.execute("UPDATE hook_runs SET details=? WHERE id=?", (json.dumps(self.details), self.id))

    def finish(self, status="completed", **details):
        self.update(**details)
        with connect() as db:
            db.execute("UPDATE hook_runs SET status=?, finished_at=? WHERE id=?", (status, time.time(), self.id))
