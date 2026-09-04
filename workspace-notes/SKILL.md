---
name: workspace-notes
description: Create a concise learning note in the current workspace's notes/ directory with a YAML read_when header and a clear filename. Use when the user says "add that to notes", "note that", "write that down for future reference", "looks like you learned something useful while doing the work please write it down for future reference", or similar requests to capture learnings.
---

# Workspace Notes

## Workflow

1. Identify the learning or reusable insight that should be preserved.
2. Create a new Markdown file under `notes/` in the current workspace.
3. Use a descriptive, kebab-case filename (e.g., `admin-routing-and-ai-toggle.md`).
4. Add a YAML header with `read_when` entries that describe when to consult the note.
5. Write concise, actionable content that future AI agents can use.

## Example Output Template

```md
---
read_when:
  - <short trigger phrase>
  - <another trigger phrase>
---

# <Short Title>
- <concise description>

## Conventions
- Keep notes short and skimmable.
- Prefer bullets over paragraphs.
- Avoid sensitive data or secrets.
