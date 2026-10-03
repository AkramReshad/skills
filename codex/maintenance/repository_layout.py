#!/usr/bin/env python3
"""Select repository directories with Jev and maintain them with the Codex SDK."""

import argparse
import json
import os
from pathlib import Path
import ssl
import subprocess
import urllib.request

import certifi


SKILL_PATH = Path(__file__).resolve().parents[2] / "maintain-repository-layout/SKILL.md"
CONVENTION_FILES = {"CONVENTIONS.md", "conventions.md", "architecture.md"}
CONFIG_FILES = {
    "package.json", "pyproject.toml", "tsconfig.json", "jsconfig.json",
    "next.config.js", "next.config.mjs", "next.config.ts",
}


def collect_state(root, skill_path):
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root, text=True,
    ).split("\0")
    directories = {".": {"direct_files": [], "direct_subdirectories": []}}
    conventions = {}
    for value in sorted(set(filter(None, paths))):
        path = Path(value)
        if not (root / path).is_file():
            continue
        parent = path.parent
        directories.setdefault(parent.as_posix(), {"direct_files": [], "direct_subdirectories": []})
        directories[parent.as_posix()]["direct_files"].append(path.name)
        while parent != Path("."):
            ancestor = parent.parent
            entry = directories.setdefault(ancestor.as_posix(), {"direct_files": [], "direct_subdirectories": []})
            if parent.name not in entry["direct_subdirectories"]:
                entry["direct_subdirectories"].append(parent.name)
            parent = ancestor
        if path.name in CONVENTION_FILES or path.name in CONFIG_FILES:
            conventions[value] = (root / path).read_text()
    for entry in directories.values():
        entry["direct_files"].sort()
        entry["direct_subdirectories"].sort()
    return {
        "layout_skill": {"name": "maintain-repository-layout", "text": skill_path.read_text()},
        "repository": {
            "directory_tree": sorted(directories),
            "structural_conventions": conventions,
        },
        "directories": dict(sorted(directories.items())),
    }


def select_directories(state):
    directory_paths = list(state["directories"])
    questions = {
        f"directory_{index}": {
            "type": "choice",
            "instructions": {
                "directory": path,
                "question": (
                    "Does the directory named in `directory` need any file organization "
                    "or naming changes under `state.layout_skill.text`, including its "
                    "examples and applicable `state.repository.structural_conventions`? "
                    "Evaluate its direct files using `state.directories`, its complete "
                    "ancestor path, sibling filenames, and existing subdirectories."
                ),
            },
            "criteria": {
                "maintain": "The rules call for at least one file organization or naming change in this directory.",
                "leave": "This directory's current files should remain as they are under the supplied rules and conventions.",
            },
        }
        for index, path in enumerate(directory_paths)
    }
    request = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps({"model": "jev-latest", "state": state, "questions": questions}).encode(),
        headers={"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}", "Content-Type": "application/json"},
        method="POST",
    )
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, timeout=120, context=context) as response:
        result = json.load(response)
    targets = []
    for index, path in enumerate(directory_paths):
        answer = result["answers"][f"directory_{index}"]
        print(json.dumps({"directory": path, **answer}), flush=True)
        if answer["choice"] == "maintain":
            targets.append(path)
    print(json.dumps({"directories_checked": len(directory_paths), "directories_selected": len(targets), "usage": result.get("usage")}), flush=True)
    return targets


def maintain_directories(root, targets, skill_path):
    from openai_codex import Codex, CodexConfig, Sandbox, SkillInput, TextInput

    with Codex(CodexConfig(config_overrides=("features.hooks=false",))) as codex:
        thread = codex.thread_start(cwd=str(root), ephemeral=True, sandbox=Sandbox.workspace_write)
        result = thread.run([
            SkillInput(name="maintain-repository-layout", path=str(skill_path)),
            TextInput(text="$maintain-repository-layout\n\nTarget directories (direct files):\n" + json.dumps(targets)),
        ])
        print(result.final_response, flush=True)


def run(root, skill_path=SKILL_PATH):
    state = collect_state(root, skill_path)
    targets = select_directories(state)
    if targets:
        maintain_directories(root, targets, skill_path)
    return targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    run(args.repository.resolve())


if __name__ == "__main__":
    main()
