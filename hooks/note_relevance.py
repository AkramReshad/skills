import json
import os
import pwd
import ssl
import subprocess
import urllib.request

import certifi


API_URL = "https://api.typesafe.ai/v1/systemone"
RELEVANCE_CUTOFF = 0.85


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
                "question": "Would including this note give the assistant useful context for answering the final user message in `state.messages`?",
                "note": content,
            },
        }
        for index, (_path, content) in enumerate(notes)
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
