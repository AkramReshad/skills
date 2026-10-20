import asyncio
import json

from note_pass import INSTRUCTIONS, NoteChanges, conversation_text

NAME = "claude"
NOTE_PASS_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(npx prettier:*)", "Bash(prettier:*)"]


def message_text(content):
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    return "\n".join(
        item["text"]
        for item in content
        if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str)
    ).strip()


def conversation_from_transcript(path, note_pass=False):
    messages = []
    with path.open(encoding="utf-8", errors="replace") as transcript:
        for line in transcript:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict) or record.get("isSidechain"):
                continue
            if record.get("type") == "system" and record.get("subtype") == "compact_boundary":
                if note_pass:
                    messages.clear()
                continue
            if record.get("type") not in {"user", "assistant"}:
                continue
            if record.get("isMeta") or record.get("isCompactSummary"):
                continue
            message = record.get("message")
            if not isinstance(message, dict) or message.get("role") not in {"user", "assistant"}:
                continue
            content = message_text(message.get("content"))
            if content:
                messages.append({"role": message["role"], "text": content})
    return messages


async def stream_note_pass(cwd, conversation, activity):
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
    changes = NoteChanges(cwd, activity, "sdk_tool_events")
    pending = {}
    prompt = f"/workspace-notes\n\n{INSTRUCTIONS}\n\n{conversation_text(conversation)}"
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in {"Write", "Edit"}:
                    path = cwd / block.input.get("file_path", "")
                    pending[block.id] = ("add" if block.name == "Write" and not path.exists() else "update", path)
        elif isinstance(message, UserMessage) and isinstance(message.content, list):
            for block in message.content:
                if isinstance(block, ToolResultBlock) and block.tool_use_id in pending:
                    kind, path = pending.pop(block.tool_use_id)
                    if not block.is_error:
                        changes.record(kind, path)
        elif isinstance(message, ResultMessage):
            activity.update(agent_session_id=message.session_id, cost_usd=message.total_cost_usd)
            if message.is_error:
                raise RuntimeError(f"Note capture ended with {message.subtype}: {message.result or ''}".strip())
    return changes.created_count


def run_note_pass(cwd, conversation, activity):
    return asyncio.run(stream_note_pass(cwd, conversation, activity))
