#!/usr/bin/env python3

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import shared  # noqa: F401
from claude_transcript import conversation_from_transcript
from hook_activity import HookRun


NOTE_PASS_TIMEOUT = 570
NOTE_PASS_TOOLS = ["Skill", "Read", "Write", "Edit", "Glob", "Grep", "Bash(npx prettier:*)", "Bash(prettier:*)"]


def hook_result(message=None):
    result = {"continue": True}
    if message:
        result["systemMessage"] = f"Precompaction notes: {message}"
    print(json.dumps(result))


def note_snapshot(notes_dir):
    return {
        str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in notes_dir.glob("*.md")
        if path.is_file()
    }


def run_note_pass(cwd, conversation, activity):
    notes_dir = cwd / "notes"
    before = note_snapshot(notes_dir)
    prompt = (
        "Use the workspace-notes skill to capture learnings from the conversation below.\n\n"
        "After writing the notes, run Prettier with --write on the note files you created or updated, "
        "using the workspace's Prettier configuration.\n\n"
        + "\n\n".join(f"{message['role'].upper()}:\n{message['text']}" for message in conversation)
    )
    environment = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}
    activity.update(phase="writing_notes", count_source="notes_directory_snapshot", created_count=0,
                    created_notes=[], modified_notes=[], deleted_notes=[])
    result = subprocess.run(
        ["claude", "-p", "--no-session-persistence", "--settings", json.dumps({"disableAllHooks": True}),
         "--permission-mode", "acceptEdits", "--allowedTools", *NOTE_PASS_TOOLS, "--output-format", "json"],
        input=prompt, text=True, capture_output=True, cwd=cwd, env=environment,
        timeout=NOTE_PASS_TIMEOUT, check=False,
    )
    after = note_snapshot(notes_dir)
    created = sorted(after.keys() - before.keys())
    modified = sorted(path for path in after.keys() & before.keys() if after[path] != before[path])
    deleted = sorted(before.keys() - after.keys())
    activity.update(created_count=len(created), created_notes=created,
                    modified_notes=modified, deleted_notes=deleted)
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = {}
    if result.returncode != 0 or output.get("is_error"):
        detail = output.get("result") or result.stderr.strip() or f"exit status {result.returncode}"
        raise RuntimeError(f"Note capture failed: {detail}")
    activity.update(agent_session_id=output.get("session_id"), cost_usd=output.get("total_cost_usd"))
    return len(created)


def main(activity):
    event = json.load(sys.stdin)
    activity.event(event)
    if event.get("hook_event_name") != "PreCompact":
        raise RuntimeError("Unexpected hook event")
    cwd = Path(event["cwd"]).expanduser().resolve(strict=True)
    transcript_value = event.get("transcript_path")
    if not transcript_value:
        raise RuntimeError("No transcript was provided")
    transcript = Path(transcript_value).expanduser().resolve(strict=True)
    if not transcript.is_file():
        raise RuntimeError("Transcript is unavailable")
    notes_dir = cwd / "notes"
    if not notes_dir.resolve().is_relative_to(cwd):
        raise RuntimeError("Workspace notes directory resolves outside the workspace")
    activity.update(client="claude", phase="reading_transcript", notes_directory=str(notes_dir))
    conversation = conversation_from_transcript(transcript, since_compaction=True)
    activity.update(message_count=len(conversation))
    if not conversation:
        activity.finish("skipped", reason="no_conversation_messages")
        hook_result("No user or assistant messages could be extracted from the transcript")
        return
    created_count = run_note_pass(cwd, conversation, activity)
    activity.finish(reason="notes_created" if created_count else "no_note_creations_reported")
    hook_result()


if __name__ == "__main__":
    activity = HookRun("PreCompact")
    try:
        main(activity)
    except Exception as exc:
        activity.finish("error", error=str(exc))
        hook_result(str(exc))
