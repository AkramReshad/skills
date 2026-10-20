import json
import os
from pathlib import Path

from note_pass import INSTRUCTIONS, NoteChanges, conversation_text

NAME = "codex"


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


def conversation_from_transcript(path, note_pass=False):
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
            if note_pass and (record_type == "compacted" or (
                record_type == "response_item" and payload.get("type") == "compaction"
            )):
                messages.clear()
                event_messages.clear()
                continue
            if record_type == "response_item" and payload.get("type") == "message":
                role = payload.get("role")
                if role in {"user", "assistant"}:
                    content = message_text(payload.get("content"))
                    if content:
                        messages.append({"role": role, "text": content})
            elif note_pass and record_type == "response_item" and payload.get("type") == "agent_message":
                content = message_text(payload.get("content"))
                if content:
                    messages.append({"role": "assistant", "author": payload.get("author", "agent"), "text": content})
            elif record_type == "event_msg":
                role = {"user_message": "user", "agent_message": "assistant"}.get(payload.get("type"))
                content = payload.get("message")
                if role and isinstance(content, str) and content.strip():
                    event_messages.append({"role": role, "text": content.strip()})
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
        activity.update(agent_thread_id=thread.id)
        changes = NoteChanges(cwd, activity, "sdk_file_change_events")
        turn = thread.turn([
            SkillInput(name="workspace-notes", path=str(skill_path)),
            TextInput(text=f"$workspace-notes\n\n{INSTRUCTIONS}\n\n{conversation_text(conversation)}"),
        ])
        for event in turn.stream():
            payload = event.payload
            if isinstance(payload, ItemCompletedNotification):
                item = payload.item.root
                if isinstance(item, FileChangeThreadItem) and item.status == PatchApplyStatus.completed:
                    for change in item.changes:
                        changes.record(change.kind.root.type, change.path)
            elif isinstance(payload, TurnCompletedNotification):
                if payload.turn.status == TurnStatus.failed:
                    raise RuntimeError(payload.turn.error.message if payload.turn.error else "Note capture failed")
                if payload.turn.status != TurnStatus.completed:
                    raise RuntimeError(f"Note capture ended with status {payload.turn.status.value}")
        return changes.created_count
