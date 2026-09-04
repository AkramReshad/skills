---
name: issue-tools
description: Create GitHub issues using gh issue for code problems or backlog ideas. Use when the user says "add issue", "create issue", or "add that to the backlog".
---

# Issue Tools

Create issues using the exact behavior of the legacy commands:
- `.claude/commands/add-issue.md`
- `.claude/commands/backlog.md`

Always use `gh issue create`.

## When to use

- User says: "add issue" or "create issue" -> use the Add Issue workflow.
- User says: "add that to the backlog" -> use the Backlog workflow.

## References

- Use scopes from `docs/project_management/scopes-reference.md`.
- Use issue templates in `.github/ISSUE_TEMPLATE/` (task.md, story.md).
- Match the style in `tasks/issues.md`.
- Full label list: `issue-tools/labels.md`.

## Add Issue workflow (exact behavior)

1. **Parse input**
   - Extract problem and `file:line` location
   - Determine: bug, enhancement, or technical-debt
   - Single fix = `task`, needs investigation = `story`

2. **Read references**
   - `docs/project_management/scopes-reference.md` for component label
   - `.github/ISSUE_TEMPLATE/task.md` or `.github/ISSUE_TEMPLATE/story.md`

3. **Read code context** if `file:line` given (5 lines before/after)

4. **Determine labels**
   - `type:task` or `type:story`
   - `bug`, `enhancement`, or `technical-debt`
   - `priority:low/medium/high/critical`
   - Component label from scopes-reference.md

5. **Format body** (match `tasks/issues.md` style)
   ```
   **Issue**: [Problem with `file:line` location]
   **Fix**: [Clear action to resolve]

   Related to: #9
   ```

6. **Create issue**
   ```bash
   gh issue create \
     --title "[Problem summary]" \
     --body "[formatted body]" \
     --label "[labels]"
   ```

7. **Output**
   ```
   📝 Issue #[number] created
   Title: [title]
   Labels: [labels]
   Link: [url]

   For commits: "Fixes #[number]" or "Relates to #[number]"
   ```

## Backlog workflow (exact behavior)

1. Read `docs/project_management/scopes-reference.md` and pick one component label

2. Create issue with `backlog` + component label:
   ```bash
   gh issue create \
     --title "{{input}}" \
     --body "Review during sprint planning" \
     --label "backlog,{{component}}"
   ```

3. Output: `✅ #{{number}}`
