#!/usr/bin/env python3

import json
from pathlib import Path
import sys

from load_relevant_notes import is_subagent_transcript, state_path


def main():
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "PostCompact":
        raise RuntimeError("Unexpected hook event")
    cwd = Path(event["cwd"]).expanduser().resolve(strict=True)
    transcript_path = event.get("transcript_path")
    if transcript_path and is_subagent_transcript(Path(transcript_path).expanduser()):
        print(json.dumps({"continue": True}))
        return
    state_path(event, cwd).unlink(missing_ok=True)
    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"continue": True, "systemMessage": f"Workspace note reset: {exc}"}))
