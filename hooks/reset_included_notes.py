#!/usr/bin/env python3

import json
from pathlib import Path
import sys

import clients
from load_relevant_notes import state_path


def main(client):
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "PostCompact":
        raise RuntimeError("Unexpected hook event")
    cwd = Path(event["cwd"]).expanduser().resolve(strict=True)
    state_path(client, event, cwd).unlink(missing_ok=True)
    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    try:
        main(clients.from_arguments())
    except Exception as exc:
        print(json.dumps({"continue": True, "systemMessage": f"Workspace note reset: {exc}"}))
