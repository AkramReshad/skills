---
name: workspace-notes
description: Create a concise learning note in the current workspace's notes/ directory with a clear filename. Use when the user says "add that to notes", "note that", "write that down for future reference", "looks like you learned something useful while doing the work please write it down for future reference", or similar requests to capture learnings.
---

# Workspace Notes

## Workflow

1. Identify the learning or reusable insight that should be preserved.
2. Create a new Markdown file under `notes/` in the current workspace.
3. Use a descriptive, snake_case filename (e.g., `admin_routing_and_ai_toggle.md`).
4. Write short, succinct, actionable content that future AI agents can use. Each note should capture one focused learning or reusable insight in a few bullets, at most 150 words. Split distinct insights into separate notes.

## Example Output Template

```md
# <Short Title>
- <concise description>

```

## Conventions
- Keep notes short and skimmable.
- Prefer bullets over paragraphs.
- During consolidation, preserve short, focused notes. Merge only notes about the same specific insight when the combined result remains within 150 words. Keep distinct insights in separate files.
