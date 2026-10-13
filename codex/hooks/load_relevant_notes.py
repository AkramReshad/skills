#!/usr/bin/env python3

import json
import hashlib
import os
from pathlib import Path
import pwd
import ssl
import subprocess
import sys
import tempfile
import urllib.request

import certifi

from hook_activity import HookRun


API_URL = "https://api.typesafe.ai/v1/systemone"
RELEVANCE_CUTOFF = 0.85


def message_text(content):
    if not isinstance(content, list):
        return ""
    return "\n".join(
        item["text"]
        for item in content
        if isinstance(item, dict)
        and item.get("type") in {"input_text", "output_text", "text"}
        and isinstance(item.get("text"), str)
    ).strip()


def conversation_from_transcript(path):
    messages = []
    event_messages = []
    with path.open(encoding="utf-8", errors="replace") as transcript:
        for line in transcript:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            if record.get("type") == "response_item" and payload.get("type") == "message":
                role = payload.get("role")
                if role in {"user", "assistant"}:
                    content = message_text(payload.get("content"))
                    if content:
                        messages.append({"role": role, "text": content})
            elif record.get("type") == "event_msg":
                role = {"user_message": "user", "agent_message": "assistant"}.get(
                    payload.get("type")
                )
                content = payload.get("message")
                if role and isinstance(content, str) and content.strip():
                    event_messages.append({"role": role, "text": content.strip()})
    return messages or event_messages


def state_path(event, cwd):
    session_id = event["session_id"]
    identifier = hashlib.sha256(f"{session_id}\n{cwd}".encode("utf-8")).hexdigest()
    directory = Path(tempfile.gettempdir()) / f"codex_note_context_{os.getuid()}"
    return directory / f"{identifier}.json"


def included_notes(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return set()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise RuntimeError("Invalid included-note state")
    return set(value)


def save_included_notes(path, names):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(sorted(names)), encoding="utf-8")
    temporary.replace(path)


def typesafe_api_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    if key:
        return key
    account = pwd.getpwuid(os.getuid()).pw_name
    result = subprocess.run(
        ["security", "find-generic-password", "-a", account, "-s", "TYPESAFE_API_KEY", "-w"],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("TYPESAFE_API_KEY is unavailable from macOS Keychain")
    return result.stdout.strip()


def typesafe_request(messages, notes, api_key):
    questions = {
        f"note_{index}": {
            "type": "noul",
            "instructions": {
                "question": "Would including this note give the assistant useful context for answering the final user message in `state.messages` or continuing the active task?",
                "note": {"filename": path.name, "text": content},
            },
            "criteria": {
                "true": "The note contains a specific fact, preference, decision, or learning that could help with the current response or task.",
                "false": "The note offers no useful context for the current response or task, even if it shares a broad topic.",
            },
        }
        for index, (path, content) in enumerate(notes)
    }
    body = json.dumps(
        {"model": "jev-latest", "state": {"messages": messages}, "questions": questions}
    ).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, timeout=120, context=context) as response:
        result = json.load(response)
    answers = result.get("answers")
    if not isinstance(answers, dict):
        raise RuntimeError("TypeSafe returned no answers")
    relevant = []
    for index, note in enumerate(notes):
        answer = answers.get(f"note_{index}")
        if not isinstance(answer, dict) or answer.get("type") != "noul":
            raise RuntimeError(f"TypeSafe returned no Noul answer for note_{index}")
        probability = answer.get("noul")
        if not isinstance(probability, (int, float)) or isinstance(probability, bool):
            raise RuntimeError(f"TypeSafe returned an invalid Noul answer for note_{index}")
        if probability >= RELEVANCE_CUTOFF:
            relevant.append(note)
    return relevant


def main(activity):
    event = json.load(sys.stdin)
    activity.event(event)
    hook_event = event.get("hook_event_name")
    if hook_event != "UserPromptSubmit":
        raise RuntimeError("Unexpected hook event")
    cwd = Path(event["cwd"]).expanduser().resolve(strict=True)
    transcript_path = event.get("transcript_path")
    state = state_path(event, cwd)
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
    messages = conversation_from_transcript(Path(transcript_path).expanduser())
    prompt = event.get("prompt")
    if isinstance(prompt, str) and prompt.strip():
        if not messages or messages[-1] != {"role": "user", "text": prompt.strip()}:
            messages.append({"role": "user", "text": prompt.strip()})
    activity.update(phase="checking_relevance", message_count=len(messages))
    relevant = typesafe_request(messages, notes, api_key)
    if relevant:
        save_included_notes(state, already_included | {path.name for path, _ in relevant})
    context = "\n".join(
        f"Read notes/{path.name}" for path, _ in relevant
    )
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
    activity = HookRun("UserPromptSubmit")
    try:
        main(activity)
    except Exception as exc:
        activity.finish("error", error=str(exc))
        print(json.dumps({"continue": True, "systemMessage": f"Workspace note retrieval: {exc}"}))
