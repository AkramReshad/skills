#!/usr/bin/env python3

import json
from pathlib import Path
import sys

import clients
from hook_activity import HookRun


def hook_result(message=None):
    result = {"continue": True}
    if message:
        result["systemMessage"] = f"Precompaction notes: {message}"
    print(json.dumps(result))


def main(client, activity):
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
    activity.update(phase="reading_transcript", notes_directory=str(notes_dir))
    conversation = client.conversation_from_transcript(transcript, note_pass=True)
    activity.update(message_count=len(conversation))
    if not conversation:
        activity.finish("skipped", reason="no_conversation_messages")
        hook_result("No user or assistant messages could be extracted from the transcript")
        return
    created_count = client.run_note_pass(cwd, conversation, activity)
    activity.finish(reason="notes_created" if created_count else "no_note_creations_reported")
    hook_result()


if __name__ == "__main__":
    activity = None
    try:
        client = clients.from_arguments(sys.argv[1:])
        activity = HookRun("PreCompact", client.NAME)
        main(client, activity)
    except Exception as exc:
        if activity:
            activity.finish("error", error=str(exc))
        hook_result(str(exc))
