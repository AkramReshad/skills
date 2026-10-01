#!/usr/bin/env python3

import json
import os
from pathlib import Path
import sys


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
            elif record_type == "event_msg":
                role = {"user_message": "USER", "agent_message": "ASSISTANT"}.get(
                    payload.get("type")
                )
                content = payload.get("message")
                if role and isinstance(content, str) and content.strip():
                    event_messages.append(f"{role}:\n{content.strip()}")
    return messages or event_messages


def is_subagent_transcript(path):
    with path.open(encoding="utf-8", errors="replace") as transcript:
        for line in transcript:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("type") == "session_meta":
                payload = record.get("payload")
                return isinstance(payload, dict) and bool(payload.get("parent_thread_id"))
    return False


def run_note_pass(cwd, conversation):
    from openai_codex import Codex, CodexConfig, Sandbox, SkillInput, TextInput

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    skill_path = codex_home / "skills/workspace-notes/SKILL.md"
    with Codex(CodexConfig(config_overrides=("features.hooks=false",))) as codex:
        thread = codex.thread_start(
            cwd=str(cwd),
            ephemeral=True,
            sandbox=Sandbox.workspace_write,
        )
        thread.run([
            SkillInput(name="workspace-notes", path=str(skill_path)),
            TextInput(text="$workspace-notes\n\n" + "\n\n".join(conversation)),
        ])


def main():
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "PreCompact":
        raise RuntimeError("Unexpected hook event")
    cwd = Path(event["cwd"]).expanduser().resolve(strict=True)
    transcript_value = event.get("transcript_path")
    if not transcript_value:
        raise RuntimeError("No transcript was provided")
    transcript = Path(transcript_value).expanduser().resolve(strict=True)
    if not transcript.is_file():
        raise RuntimeError("Transcript is unavailable")
    if is_subagent_transcript(transcript):
        hook_result()
        return
    notes_dir = cwd / "notes"
    if not notes_dir.resolve().is_relative_to(cwd):
        raise RuntimeError("Workspace notes directory resolves outside the workspace")
    conversation = conversation_from_transcript(transcript)
    if not conversation:
        hook_result("No user or assistant messages could be extracted from the transcript")
        return
    run_note_pass(cwd, conversation)
    hook_result()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        hook_result(str(exc))
