#!/usr/bin/env python3

import json
import hashlib
import os
from pathlib import Path
import sys
import tempfile

import clients
from hook_activity import HookRun
from note_relevance import included_notes, save_included_notes, typesafe_api_key, typesafe_request


def state_path(client, event, cwd):
    session_id = event["session_id"]
    identifier = hashlib.sha256(f"{session_id}\n{cwd}".encode("utf-8")).hexdigest()
    directory = Path(tempfile.gettempdir()) / f"{client.NAME}_note_context_{os.getuid()}"
    return directory / f"{identifier}.json"


def main(client, activity):
    event = json.load(sys.stdin)
    activity.event(event)
    if event.get("hook_event_name") != "UserPromptSubmit":
        raise RuntimeError("Unexpected hook event")
    cwd = Path(event["cwd"]).expanduser().resolve(strict=True)
    transcript_path = event.get("transcript_path")
    state = state_path(client, event, cwd)
    notes_dir = cwd / "notes"
    activity.update(notes_directory=str(notes_dir), phase="reading_notes")
    if not notes_dir.is_dir():
        activity.finish("skipped", reason="no_notes_directory")
        print(json.dumps({"continue": True}))
        return
    already_included = included_notes(state)
    notes = [
        (path, path.read_text(encoding="utf-8"))
        for path in sorted(notes_dir.glob("*.md"))
        if path.name not in already_included
    ]
    activity.update(candidate_count=len(notes), already_included_count=len(already_included))
    if not notes:
        activity.finish("skipped", reason="no_unincluded_notes")
        print(json.dumps({"continue": True}))
        return
    api_key = typesafe_api_key()
    if not transcript_path:
        raise RuntimeError("No transcript was provided")
    transcript = Path(transcript_path).expanduser()
    messages = client.conversation_from_transcript(transcript) if transcript.is_file() else []
    prompt = event.get("prompt")
    if isinstance(prompt, str) and prompt.strip():
        if not messages or messages[-1] != {"role": "user", "text": prompt.strip()}:
            messages.append({"role": "user", "text": prompt.strip()})
    activity.update(phase="checking_relevance", message_count=len(messages))
    relevant = typesafe_request(messages, notes, api_key)
    if relevant:
        save_included_notes(state, already_included | {path.name for path, _ in relevant})
    context = "\n".join(f"Read notes/{path.name}" for path, _ in relevant)
    result = {"continue": True}
    if context:
        result["hookSpecificOutput"] = {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    activity.finish(reason="context_returned" if context else "no_relevant_notes",
                    selected_notes=[str(path) for path, _ in relevant],
                    selected_count=len(relevant), context_characters=len(context))
    print(json.dumps(result))


if __name__ == "__main__":
    client = clients.from_arguments()
    activity = HookRun("UserPromptSubmit", client.NAME)
    try:
        main(client, activity)
    except Exception as exc:
        activity.finish("error", error=str(exc))
        print(json.dumps({"continue": True, "systemMessage": f"Workspace note retrieval: {exc}"}))
