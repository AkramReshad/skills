from __future__ import annotations

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "commit-consolidated-notes.sh"
ORIGINAL = "# Insight\n\n- Original fact.\n"
CONSOLIDATED = "# Insight\n\n- Consolidated facts.\n"
CORRECTION = "# Insight\n\n- New user correction.\n"


class CommitConsolidatedNotesTests(unittest.TestCase):
    def setUp(self) -> None:
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        self.remote = self.root / "remote.git"
        self.worker = self.root / "working copy"
        self.peer = self.root / "peer"
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GITHUB_REF_NAME": "main",
            "RUNNER_TEMP": str(self.artifacts),
        }
        self.git(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.clone(self.worker)
        self.write(self.worker, "notes/insight.md", ORIGINAL)
        self.commit(self.worker, "Initial notes")
        self.git(self.worker, "push", "origin", "main")
        self.initial_head = self.git(self.worker, "rev-parse", "HEAD").strip()
        self.clone(self.peer)

    def git(self, repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args], cwd=repo, env=self.env,
            check=True, capture_output=True, text=True,
        )
        return result.stdout

    def clone(self, path: Path) -> None:
        self.git(self.root, "clone", str(self.remote), str(path))
        self.git(path, "config", "user.name", "Contributor")
        self.git(path, "config", "user.email", "contributor@example.test")

    def write(self, repo: Path, name: str, content: str) -> None:
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, repo: Path, message: str) -> None:
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-m", message)

    def publish(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT)], cwd=self.worker, env=self.env,
            capture_output=True, text=True,
        )

    def test_integrates_new_main_code_and_notes_without_losing_consolidation(self) -> None:
        self.write(self.worker, "notes/insight.md", CONSOLIDATED)
        self.write(self.peer, "application.txt", "New application revision\n")
        self.write(self.peer, "notes/new_during_run.md", "# New insight\n\n- New fact.\n")
        self.commit(self.peer, "Work during consolidation")
        self.git(self.peer, "push", "origin", "main")

        result = self.publish()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git(self.remote, "show", "main:notes/insight.md"), CONSOLIDATED)
        self.assertEqual(self.git(self.remote, "show", "main:application.txt"), "New application revision\n")
        self.assertEqual(self.git(self.remote, "show", "main:notes/new_during_run.md"), "# New insight\n\n- New fact.\n")
        self.assertEqual(self.git(self.remote, "log", "-1", "--format=%s", "main"), "Consolidate workspace notes\n")

    def test_retries_when_main_moves_between_fetch_and_push(self) -> None:
        self.write(self.worker, "notes/insight.md", CONSOLIDATED)
        self.write(self.peer, "application.txt", "Concurrent application revision\n")
        self.commit(self.peer, "Concurrent update")
        marker = self.root / "peer-pushed"
        hook = self.worker / ".git/hooks/pre-push"
        hook.write_text(
            "#!/usr/bin/env bash\nset -eu\n"
            f"if [[ ! -f {shlex.quote(str(marker))} ]]; then\n"
            f"  touch {shlex.quote(str(marker))}\n"
            f"  git --git-dir={shlex.quote(str(self.peer / '.git'))} push origin main\n"
            "fi\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)

        result = self.publish()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git(self.remote, "show", "main:notes/insight.md"), CONSOLIDATED)
        self.assertEqual(self.git(self.remote, "show", "main:application.txt"), "Concurrent application revision\n")

    def test_conflicting_edit_preserves_remote_and_a_recoverable_patch(self) -> None:
        self.write(self.worker, "notes/insight.md", CONSOLIDATED)
        self.write(self.peer, "notes/insight.md", CORRECTION)
        self.commit(self.peer, "Correct the insight")
        self.git(self.peer, "push", "origin", "main")
        peer_head = self.git(self.peer, "rev-parse", "HEAD")

        result = self.publish()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), peer_head)
        self.assertEqual(self.git(self.remote, "show", "main:notes/insight.md"), CORRECTION)
        self.assertEqual((self.worker / "notes/insight.md").read_text(), CONSOLIDATED)
        recovery = self.root / "recovery"
        self.clone(recovery)
        self.git(recovery, "checkout", self.initial_head)
        self.git(recovery, "apply", str(self.artifacts / "consolidated-notes.patch"))
        self.assertEqual((recovery / "notes/insight.md").read_text(), CONSOLIDATED)


if __name__ == "__main__":
    unittest.main()
