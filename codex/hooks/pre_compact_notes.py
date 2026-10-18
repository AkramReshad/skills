#!/usr/bin/env python3

import json
import os
from pathlib import Path
import sys

from hook_activity import HookRun


def hook_result(message=None):
    result = {"continue": True}
    if message:
        result["systemMessage"] = f"Precompaction notes: {message}"
    print(json.dumps(result))


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
            record_type = record.get("type")
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            if record_type == "compacted" or (
                record_type == "response_item" and payload.get("type") == "compaction"
            ):
                messages.clear()
                event_messages.clear()
                continue
            if record_type == "response_item" and payload.get("type") == "message":
                role = payload.get("role")
                if role in {"user", "assistant"}:
                    content = message_text(payload.get("content"))
                    if content:
                        messages.append(f"{role.upper()}:\n{content}")
            elif record_type == "response_item" and payload.get("type") == "agent_message":
                content = message_text(payload.get("content"))
                if content:
                    messages.append(f"ASSISTANT ({payload.get('author', 'agent')}):\n{content}")
            elif record_type == "event_msg":
                role = {"user_message": "USER", "agent_message": "ASSISTANT"}.get(
                    payload.get("type")
                )
                content = payload.get("message")
                if role and isinstance(content, str) and content.strip():
                    event_messages.append(f"{role}:\n{content.strip()}")
    return messages or event_messages


def run_note_pass(cwd, conversation, activity):
    from openai_codex import Codex, CodexConfig, Sandbox, SkillInput, TextInput
    from openai_codex.generated.v2_all import FileChangeThreadItem, ItemCompletedNotification, PatchApplyStatus, TurnCompletedNotification, TurnStatus

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    skill_path = codex_home / "skills/workspace-notes/SKILL.md"
    with Codex(CodexConfig(config_overrides=("features.hooks=false",))) as codex:
        thread = codex.thread_start(
            cwd=str(cwd),
            ephemeral=True,
            sandbox=Sandbox.workspace_write,
        )
        activity.update(phase="writing_notes", agent_thread_id=thread.id)
        created, modified, deleted = set(), set(), set()
        activity.update(count_source="sdk_file_change_events", created_count=0, created_notes=[], modified_notes=[], deleted_notes=[])
        turn = thread.turn([
            SkillInput(name="workspace-notes", path=str(skill_path)),
            TextInput(text=(
                "$workspace-notes\n\n"
                "After writing the notes, run Prettier with --write on the note files you created or updated, "
                "using the workspace's Prettier configuration.\n\n"
                + "\n\n".join(conversation)
            )),
        ])
        for event in turn.stream():
            payload = event.payload
            if isinstance(payload, ItemCompletedNotification):
                item = payload.item.root
                if isinstance(item, FileChangeThreadItem) and item.status == PatchApplyStatus.completed:
                    for change in item.changes:
                        path = (cwd / change.path).resolve()
                        if path.suffix != ".md" or not path.is_relative_to(cwd / "notes"):
                            continue
                        kind = change.kind.root.type
                        {"add": created, "update": modified, "delete": deleted}[kind].add(str(path))
                    activity.update(created_count=len(created), created_notes=sorted(created),
                                    modified_notes=sorted(modified), deleted_notes=sorted(deleted))
            elif isinstance(payload, TurnCompletedNotification):
                if payload.turn.status == TurnStatus.failed:
                    raise RuntimeError(payload.turn.error.message if payload.turn.error else "Note capture failed")
                if payload.turn.status != TurnStatus.completed:
                    raise RuntimeError(f"Note capture ended with status {payload.turn.status.value}")
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
    activity.update(phase="reading_transcript", notes_directory=str(notes_dir))
    conversation = conversation_from_transcript(transcript)
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
