---
name: maintain-repository-layout
description: Audit and reorganize repository paths, filenames, semantic file groupings, and crowded directories. Use when repository layout cleanup, filename normalization, or structural hygiene is the primary task, or when explicitly invoked by a scheduled repository-hygiene workflow. Do not select this skill merely because ordinary implementation creates, edits, renames, moves, or deletes files.
---

# Maintain Repository Layout

Treat every repository-relative path as a semantic address. Organize files comprehensively within the requested scope while preserving existing directory boundaries and the meanings already expressed by filenames.

## Respect authority and scope

Apply these sources in order:

1. Follow explicit user instructions.
2. Follow applicable repository instructions, documented conventions, framework requirements, build constraints, and routing constraints.
3. Preserve every existing directory and explicit repository layout constraint.
4. Apply the rules below where the repository leaves room for judgment.

During ordinary implementation, clean every touched directory. During an explicit layout audit, inspect the full requested scope and apply every qualifying organization change regardless of diff size. Leave unrelated areas unchanged.

## Classify without reading candidate contents

- Classify, group, and rename candidate files using only their paths, filenames, extensions, sibling names, and existing directory structure.
- Do not open or read candidate file bodies, headings, frontmatter, embedded metadata, or Git history to determine their meaning, category, or naming accuracy.
- Assume every semantic token in an existing filename accurately describes the file.
- Do not broaden, narrow, reinterpret, or replace a filename's meaning based on file contents.
- Read repository instructions, convention files, framework configuration, and tool configuration only to learn structural constraints and protected paths.
- After paths are finalized, search and read files that reference moved paths solely to repair imports, exports, routes, manifests, links, scripts, configuration, fixtures, and tests. Do not use reference contents to reconsider candidate classification.

## Preserve existing directories

- Treat every existing directory as an intentional semantic boundary regardless of its file count.
- Never flatten, delete, collapse, rename, or relocate an existing directory during autonomous layout maintenance.
- Never move a file upward out of its current directory or laterally into another existing directory.
- Preserve empty directories, `.gitkeep` files, and directories containing only one or two files.
- Rename a file in place or move it deeper into a newly created subdirectory beneath its current parent.
- Create a new organizational directory only when at least three sibling files belong to that semantic grouping.
- Require every newly created directory to receive at least three qualifying sibling files when created.
- Do not apply the three-file threshold to existing directories.

Preserve these exact automation addresses unless the user explicitly requests an atomic workflow migration:

- `docs/codebase_architecture.md`
- `docs/codebase_domains.md`

## Organize semantic groups

- Treat the full path as the file's complete name and address.
- Make each path segment add one useful semantic fact.
- Identify stable groupings from semantic tokens and patterns visible in sibling filenames.
- Treat repeated prefixes, suffixes, and other consistent filename components as grouping signals.
- Require both a meaningful semantic relationship and at least three sibling files before creating a directory.
- Inspect a crowded directory, typically around ten or more direct files, for qualifying groups. Crowding alone does not authorize a new directory.
- Keep files flat when they are semantically independent or when a possible group contains fewer than three files.
- Apply every qualifying group in the requested scope; do not limit cleanup merely to minimize the diff.
- Prefer `snake_case` for ordinary filenames unless the language, framework, toolchain, or repository uses another convention.
- Preserve filenames and colocations required by the language, framework, toolchain, generated layout, route system, migration system, or test system.

## Rename by transferring semantics into the path

Assume every filename token is intentional. Remove a token only when the path takes over that same semantic responsibility:

1. Promote a semantic token shared by at least three sibling files into a newly created directory, then remove that promoted token from those filenames.
2. Remove information already supplied by an existing ancestor directory when the redundancy is evident from the filename and path alone. Treat a generic file-role token as inherited when the ancestor path already defines that artifact context, even if the token is not a literal lexical duplicate of the directory name.

Allow mechanical normalization of separators and casing without changing semantic tokens. Do not remove qualifiers, substitute synonyms, or rename a file to match the apparent scope of its contents.

## Perform and verify changes

1. Read applicable repository instructions and structural configuration.
2. Record the existing directory tree so every original directory can be verified afterward.
3. Inspect candidate paths and filenames without opening candidate files.
4. Identify every qualifying group and exact mechanical rename in the requested scope.
5. Prefer `git mv` for tracked files.
6. Repair every affected reference after the final paths are known.
7. Search for stale paths and names.
8. Verify that every pre-existing directory still exists and that each newly created directory began with at least three qualifying sibling files.
9. Verify that protected automation addresses remain unchanged.
10. Run the repository's relevant formatting, type, build, and test checks.
11. Review the resulting tree and complete diff for semantic loss, directory regression, accidental duplication, or unrelated movement.

## Examples

### Promote a shared subject

Bad:

```text
planning/project/
├── agent_output_viewer_brief.md
├── agent_runtime_plan.md
└── agent_telemetry_brief.md
```

Good:

```text
planning/project/
└── agent/
    ├── output_viewer.md
    ├── runtime.md
    └── telemetry.md
```

The `agent` token moves into the new directory. The existing `planning/` ancestor already supplies the artifact context expressed by `plan` and `brief`, so those role tokens also leave the basenames.

### Promote a shared suffix

Bad:

```text
docs/
├── api_metrics.md
├── agent_metrics.md
└── runtime_metrics.md
```

Good:

```text
docs/
└── metrics/
    ├── api.md
    ├── agent.md
    └── runtime.md
```

### Preserve a singleton's meaning

Bad:

```text
docs/agent-telemetry-metrics.md
```

Good:

```text
docs/agent_telemetry_metrics.md
```

Do not create `docs/agents/` for one file or remove `metrics` by interpreting the document body.

### Preserve sparse directories

Keep this existing structure unchanged:

```text
brand/logos/
└── mark/
    ├── blue.png
    └── white.png
```

The skill does not flatten or remove existing directories.
