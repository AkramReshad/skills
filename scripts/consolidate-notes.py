#!/usr/bin/env python3
"""Consolidate notes added to the default branch on the previous local day."""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, time as day_time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


TIMEZONE = ZoneInfo("America/Los_Angeles")
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"
COMMIT_SUBJECT = "Consolidate workspace notes"
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
CRITERIA = {
    "duplicate": "The new note adds no useful information beyond the existing note; remove the new note.",
    "supersedes": "The new note fully replaces the existing note, including its useful information and any correction or update; remove the existing note.",
    "merge": "The notes contain complementary useful information best kept together in one note; combine their content.",
    "separate": "The notes are useful as separate notes, even if they concern a related topic; keep both.",
}


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def added_notes_for_day(day):
    start = datetime.combine(day, day_time.min, TIMEZONE)
    end = start + timedelta(days=1)
    commits = git(
        "log", "--first-parent", "--reverse", "--format=%H%x09%ae",
        f"--since={start.isoformat()}", f"--before={end.isoformat()}",
    )
    additions = []
    seen = set()
    active_commits = 0
    for entry in commits.splitlines():
        commit, email = entry.split("\t", 1)
        if email == BOT_EMAIL:
            continue
        active_commits += 1
        try:
            parent = git("rev-parse", f"{commit}^1")
        except subprocess.CalledProcessError:
            parent = EMPTY_TREE
        changes = git("diff", "--no-renames", "--name-status", parent, commit, "--", "notes")
        for change in changes.splitlines():
            status, path = change.split("\t", 1)
            note = Path(path)
            if status == "A" and note.parts[0] == "notes" and note.suffix == ".md" and path not in seen:
                additions.append(path)
                seen.add(path)
    return active_commits, additions


def evaluate(new_note, existing):
    questions = {}
    for index, (path, content) in enumerate(existing):
        questions[str(index)] = {
            "type": "choice",
            "instructions": {
                "question": "How should the new workspace note relate to this existing workspace note?",
                "existing_note_path": path,
                "existing_note": content,
                "new_note_reference": "Compare with `state.new_note`.",
            },
            "criteria": CRITERIA,
        }
    payload = json.dumps({"model": "jev-latest", "state": {"new_note": new_note}, "questions": questions}).encode()
    request = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=payload,
        headers={
            "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                answers = json.load(response)["answers"]
            break
        except urllib.error.HTTPError as error:
            if error.code not in (429, 529) or attempt == 3:
                raise
            time.sleep(2 ** attempt)
    result = {}
    for index, (path, _) in enumerate(existing):
        answer = answers[str(index)]
        choice = answer["choice"]
        if answer["type"] != "choice" or choice not in CRITERIA:
            raise ValueError(f"Unexpected TypeSafe answer for {path}: {answer}")
        result[path] = choice
    return result


def merge_notes(new_content, old_contents):
    lines = new_content.rstrip().splitlines()
    existing_bullets = {line.strip().casefold() for line in lines if line.lstrip().startswith("- ")}
    for old_content in old_contents:
        old_lines = old_content.rstrip().splitlines()
        if old_lines and old_lines[0].startswith("# "):
            old_lines = old_lines[1:]
        additions = []
        for line in old_lines:
            normalized = line.strip().casefold()
            if line.lstrip().startswith("- "):
                if normalized in existing_bullets:
                    continue
                existing_bullets.add(normalized)
            additions.append(line)
        if any(line.strip() for line in additions):
            lines.extend(["", *additions])
    return "\n".join(lines).rstrip() + "\n"


def consolidate(day):
    if git("status", "--porcelain", "--", "notes"):
        raise RuntimeError("Working tree has note changes")
    active_commits, additions = added_notes_for_day(day)
    if not active_commits:
        print(f"No commits to the default branch on {day}; nothing to process")
        return
    current = {}
    tracked = git("ls-files", "-z", "--", "notes")
    for path in filter(None, tracked.split("\0")):
        file = Path(path)
        if file.suffix == ".md" and file.is_file() and not file.is_symlink():
            current[path] = file.read_text()
    new_paths = [path for path in additions if path in current]
    if not new_paths:
        print(f"No newly added notes on {day}; nothing to process")
        return
    original = current.copy()
    existing_paths = set(current) - set(new_paths)
    for new_path in new_paths:
        if new_path not in current:
            continue
        decisions = {}
        targets = sorted(existing_paths)
        for offset in range(0, len(targets), 32):
            batch = targets[offset:offset + 32]
            decisions.update(evaluate(current[new_path], [(path, current[path]) for path in batch]))
        if "duplicate" in decisions.values():
            del current[new_path]
            print(f"Removed duplicate: {new_path}")
            continue
        superseded = [path for path, choice in decisions.items() if choice == "supersedes"]
        merged = [path for path, choice in decisions.items() if choice == "merge"]
        if merged:
            current[new_path] = merge_notes(current[new_path], [current[path] for path in merged])
        for path in superseded + merged:
            del current[path]
            existing_paths.remove(path)
        existing_paths.add(new_path)
        print(f"Kept {new_path}; superseded {len(superseded)}, merged {len(merged)}")
    for path in original.keys() - current.keys():
        Path(path).unlink()
    for path, content in current.items():
        if original.get(path) != content:
            Path(path).write_text(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", help="Local date to process, YYYY-MM-DD (default: yesterday)")
    args = parser.parse_args()
    day = datetime.strptime(args.day, "%Y-%m-%d").date() if args.day else datetime.now(TIMEZONE).date() - timedelta(days=1)
    consolidate(day)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Note consolidation failed: {error}", file=sys.stderr)
        raise
