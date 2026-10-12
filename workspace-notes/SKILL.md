---
name: workspace-notes
description: Create a concise learning note in the current workspace's notes/ directory with a clear filename. Use when the user says "add that to notes", "note that", "write that down for future reference", "looks like you learned something useful while doing the work please write it down for future reference", or similar requests to capture learnings.
---

# Workspace Notes

## Workflow

1. Identify concrete learnings useful to future sessions: discoveries, causes and fixes, project behavior, technical decisions and their rationale, and user preferences. Save as many notes as you believe would be useful. Exclude generic verification instructions and temporary status updates such as progress reports, pending work, test-run totals, and completion reports. Write each learning with enough context to remain useful after the original task is finished, without requiring knowledge of that session’s history or organization.
2. Create a new Markdown file under `notes/` in the current workspace.
3. Use a descriptive, snake_case filename (e.g., `admin_routing_and_ai_toggle.md`).
4. Write short, succinct, actionable content that future AI agents can use. Each note should capture one focused learning or reusable insight in a few bullets, at most 150 words. Split distinct insights into separate notes.

## Example Output Template

```md
# <Short Title>
- <concise description>

```

## Conventions
- Record established project decisions and preferences directly, including their rationale when known. Omit personal attribution and the conversational exchange that produced them. Distinguish an adopted direction from an idea being explored: guesses, proposals, questions, and tentative thoughts should not become durable guidance unless they are subsequently adopted or validated.
- When creating notes, do not read or check existing notes. Do not worry about duplication; save the notes.
- Keep notes short and skimmable.
- Prefer bullets over paragraphs.
