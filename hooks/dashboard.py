import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from hook_activity import connect, database_path


def project_directory(cwd):
    if not cwd:
        return "Unknown"
    path = Path(cwd)
    git_file = path / ".git"
    if git_file.is_file():
        text = git_file.read_text().strip()
        if text.startswith("gitdir:"):
            git_dir = (path / text[7:].strip()).resolve()
            common = git_dir / "commondir"
            if common.is_file():
                return str((git_dir / common.read_text().strip()).resolve().parent)
    return cwd


class Dashboard(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?", 1)[0] == "/api/counts":
            db = connect()
            try:
                runs = db.execute("SELECT cwd, session_id, hook, status, details FROM hook_runs").fetchall()
            finally:
                db.close()
            groups = {}
            for cwd, session, hook, status, details in runs:
                project = project_directory(cwd)
                for key in [(project, "All sessions"), (project, session or "Unknown")]:
                    if key not in groups:
                        groups[key] = dict(project=key[0], session=key[1], capture=0, prompt=0,
                                           completed=0, skipped=0, error=0, running=0, created=0, selected=0)
                    row = groups[key]
                    row["capture" if hook == "PreCompact" else "prompt"] += 1
                    row[status] += 1
                    detail = json.loads(details)
                    row["created"] += detail.get("created_count", 0)
                    row["selected"] += detail.get("selected_count", 0)
            body = json.dumps({"rows": [groups[key] for key in sorted(groups)],
                               "database": str(database_path())}).encode()
            content_type = "application/json"
        elif self.path.split("?", 1)[0] == "/api/runs":
            db = connect()
            try:
                records = db.execute("SELECT started_at, cwd, session_id, hook, status, details FROM hook_runs ORDER BY started_at DESC").fetchall()
            finally:
                db.close()
            runs = []
            for started, cwd, session, hook, status, details in records:
                detail = json.loads(details)
                runs.append(dict(started=started, project=project_directory(cwd), cwd=cwd,
                                 session=session, hook=hook, status=status,
                                 created=(0 if status == "skipped" else detail.get("created_count")) if hook == "PreCompact" else None,
                                 shown=detail.get("selected_count", 0) if hook == "UserPromptSubmit" and status != "running" else None,
                                 result=detail.get("error") or detail.get("reason") or detail.get("phase", "")))
            body = json.dumps({"runs": runs}).encode()
            content_type = "application/json"
        elif self.path == "/":
            body = Path(__file__).with_name("dashboard.html").read_bytes()
            content_type = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    db = connect()
    db.close()
    print(f"Hook dashboard: http://127.0.0.1:{args.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Dashboard).serve_forever()
