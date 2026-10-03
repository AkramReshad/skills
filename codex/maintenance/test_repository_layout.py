import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("repository_layout", Path(__file__).with_name("repository_layout.py"))
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)


class RepositoryLayoutTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.skill = self.root / "layout_skill.md"
        self.skill.write_text("# Layout rules\nKeep existing directories.\n## Examples\nGroup three metric files.\n")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_state_contains_paths_rules_and_conventions_without_candidate_contents(self):
        self.write(".gitignore", b"generated/\nlayout_skill.md\n")
        self.write("docs/api_metrics.md", b"SECRET candidate body must not reach Jev")
        self.write("docs/agent_metrics.md", b"\xff\xfe")
        self.write("docs/runtime_metrics.md", b"text")
        self.write("brand/logos/mark/.gitkeep", b"")
        self.write("CONVENTIONS.md", b"Use snake_case for documents.")
        self.write("AGENTS.md", b"Unrelated agent instructions.")
        self.write("generated/output.md", b"ignored")
        state = layout.collect_state(self.root, self.skill)
        self.assertEqual(state["layout_skill"]["text"], self.skill.read_text())
        self.assertEqual(state["directories"]["docs"]["direct_files"], ["agent_metrics.md", "api_metrics.md", "runtime_metrics.md"])
        self.assertEqual(state["directories"]["brand/logos"]["direct_subdirectories"], ["mark"])
        self.assertEqual(state["repository"]["structural_conventions"], {"CONVENTIONS.md": "Use snake_case for documents."})
        self.assertNotIn("SECRET", json.dumps(state))
        self.assertNotIn("Unrelated agent instructions.", json.dumps(state))
        self.assertNotIn("generated", state["directories"])

    def test_one_shared_request_routes_selected_directories_without_probability_gate(self):
        state = {"layout_skill": {"text": self.skill.read_text()}, "repository": {}, "directories": {"docs": {}, "brand/logos/mark": {}}}
        response = {"answers": {
            "directory_0": {"type": "choice", "choice": "maintain", "confidence": 0.02},
            "directory_1": {"type": "choice", "choice": "leave", "confidence": 0.99},
        }, "usage": {"input_tokens": 100, "output_tokens": 20}}
        with patch.object(layout.urllib.request, "urlopen") as send, patch.dict(layout.os.environ, {"TYPESAFE_API_KEY": "test"}), patch("sys.stdout", new=io.StringIO()):
            send.return_value.__enter__.return_value = io.StringIO(json.dumps(response))
            targets = layout.select_directories(state)
        self.assertEqual(targets, ["docs"])
        self.assertEqual(send.call_count, 1)
        body = json.loads(send.call_args.args[0].data)
        self.assertEqual(body["state"], state)
        self.assertEqual(len(body["questions"]), 2)
        self.assertEqual([q["instructions"]["directory"] for q in body["questions"].values()], ["docs", "brand/logos/mark"])

    def test_only_flagged_directories_reach_codex_with_the_skill(self):
        with patch.object(layout, "collect_state", return_value={}), patch.object(layout, "select_directories", return_value=["docs"]), patch("openai_codex.Codex") as codex, patch("sys.stdout", new=io.StringIO()):
            layout.run(self.root, self.skill)
        client = codex.return_value.__enter__.return_value
        self.assertEqual(client.thread_start.call_args.kwargs["cwd"], str(self.root))
        inputs = client.thread_start.return_value.run.call_args.args[0]
        self.assertEqual(inputs[0].name, "maintain-repository-layout")
        self.assertEqual(inputs[0].path, str(self.skill))
        self.assertEqual(inputs[1].text, '$maintain-repository-layout\n\nTarget directories (direct files):\n["docs"]')
        with patch.object(layout, "collect_state", return_value={}), patch.object(layout, "select_directories", return_value=[]), patch.object(layout, "maintain_directories") as maintain:
            self.assertEqual(layout.run(self.root, self.skill), [])
        maintain.assert_not_called()


if __name__ == "__main__":
    unittest.main()
