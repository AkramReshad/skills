# Personal Agent Skills

This repository is the canonical source for personal skills. Each top-level skill directory follows the Agent Skills layout and contains a `SKILL.md` entrypoint. OpenAI-managed system skills are excluded.

## Install

Clone the repository, then link its skills into the clients used on that machine:

```bash
./scripts/link-skills codex claude
```

The linker supports these targets:

| Target | Personal skill directory |
| --- | --- |
| `codex` | `${CODEX_HOME:-$HOME/.codex}/skills` |
| `claude` | `$HOME/.claude/skills` |
| `agent` | `$HOME/.agent/skills` |
| `agents` | `$HOME/.agents/skills` |

Omit the targets to link all four locations.

On a machine that already has local copies, adopt them once:

```bash
./scripts/link-skills --dry-run --adopt
./scripts/link-skills --adopt
```

Adoption moves each conflicting entry into a timestamped directory under `$HOME/.skill-backups`, then creates the symlink. It does not delete the backup.

## Maintenance

Create and edit skills in this repository. The installed paths are symlinks, so every client reads the repository files directly.

The regular workflow is:

```bash
git pull --ff-only
$EDITOR <skill-directory>/SKILL.md
git add <skill-directory>
git commit
git push
```

On another machine, `git pull --ff-only` updates the active skills immediately. Run `scripts/link-skills` again after adding a skill; existing correct links are left unchanged.

Keep client-neutral instructions in `SKILL.md`. Client-specific metadata can remain in optional files such as `agents/openai.yaml`; clients that do not use those files ignore them.

The open Agent Skills specification defines the portable core: YAML frontmatter with `name` and `description`, followed by Markdown instructions, with optional `scripts`, `references`, and `assets` directories.
