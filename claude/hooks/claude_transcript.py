import json


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


def conversation_from_transcript(path, since_compaction=False):
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
                if since_compaction:
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
