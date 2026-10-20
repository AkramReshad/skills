#!/usr/bin/env python3

import asyncio
import json
from pathlib import Path
import sys

import shared  # noqa: F401
from claude_transcript import conversation_from_transcript
from hook_activity import HookRun


NOTE_PASS_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(npx prettier:*)", "Bash(prettier:*)"]


def hook_result(message=None):
    result = {"continue": True}
    if message:
        result["systemMessage"] = f"Precompaction notes: {message}"
    print(json.dumps(result))


async def run_note_pass(cwd, conversation, activity):
    from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolResultBlock,
                                  ToolUseBlock, UserMessage, query)

    options = ClaudeAgentOptions(
        cwd=str(cwd),
        skills=["workspace-notes"],
        allowed_tools=NOTE_PASS_TOOLS,
        permission_mode="acceptEdits",
        settings=json.dumps({"disableAllHooks": True}),
        extra_args={"no-session-persistence": None},
    )
    prompt = (
        "/workspace-notes\n\n"
        "After writing the notes, run Prettier with --write on the note files you created or updated, "
        "using the workspace's Prettier configuration.\n\n"
        + "\n\n".join(f"{message['role'].upper()}:\n{message['text']}" for message in conversation)
    )
    activity.update(phase="writing_notes", count_source="sdk_tool_events", created_count=0,
                    created_notes=[], modified_notes=[], deleted_notes=[])
    created, modified, pending = set(), set(), {}
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in {"Write", "Edit"}:
                    path = (cwd / block.input.get("file_path", "")).resolve()
                    if path.suffix == ".md" and path.is_relative_to(cwd / "notes"):
                        kind = "add" if block.name == "Write" and not path.exists() else "update"
                        pending[block.id] = (kind, str(path))
        elif isinstance(message, UserMessage) and isinstance(message.content, list):
            for block in message.content:
                if isinstance(block, ToolResultBlock) and block.tool_use_id in pending:
                    kind, path = pending.pop(block.tool_use_id)
                    if block.is_error:
                        continue
                    if kind == "add":
                        created.add(path)
                    elif path not in created:
                        modified.add(path)
            activity.update(created_count=len(created), created_notes=sorted(created),
                            modified_notes=sorted(modified), deleted_notes=[])
        elif isinstance(message, ResultMessage):
            activity.update(agent_session_id=message.session_id, cost_usd=message.total_cost_usd)
            if message.is_error:
                raise RuntimeError(f"Note capture ended with {message.subtype}: {message.result or ''}".strip())
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
    created_count = asyncio.run(run_note_pass(cwd, conversation, activity))
    activity.finish(reason="notes_created" if created_count else "no_note_creations_reported")
    hook_result()


if __name__ == "__main__":
    activity = HookRun("PreCompact")
    try:
        main(activity)
    except Exception as exc:
        activity.finish("error", error=str(exc))
        hook_result(str(exc))
