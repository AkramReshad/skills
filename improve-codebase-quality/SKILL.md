---
name: improve-codebase-quality
description: "Find all validated code quality issues in every codebase domain, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-quality or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Quality

Surface code quality issues and propose **quality improvements** — fixes grounded in current code and concrete consequences. The aim is correctness and maintainability. Review every domain and retain every validated finding; do not limit the review to one or two candidates.

## Glossary

Use these terms consistently when discussing quality. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Domain** — a review partition with a name, persona, scope, and anchor paths.
- **Issue** — a defect or concrete quality problem supported by current code.
- **Evidence** — the code, execution path, or targeted check establishing an issue and its consequence.
- **Severity** — the impact and likelihood of an issue in representative use.
- **Non-issue** — an explicitly accepted concern with a reason and revisit trigger.
- **Verification** — evidence that a proposed fix resolves its issue while preserving required behaviour.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Complete domain coverage.** Review every domain and every file in its scope.
- **Validate every finding.** Trace the code and dependencies before retaining an issue or proposing a fix.
- **Persistent issue hygiene.** Keep valid issues, remove resolved issues, and preserve accepted non-issues.
- **Verification matches the mechanism.** Specify how the fix and preserved behaviour would be checked.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to code and behaviour, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Also read existing `code_review/non-issues.md` and domain issue files.

Use the current checkout. Do not fetch, reset, clean, configure runtimes, copy skills, or refresh architecture/domain documentation.

Use `docs/codebase_domains.md` as the canonical domain/persona config. Preserve its domain names, personas, scope, and anchor paths. Read matching domain sections in `docs/codebase_architecture.md` for additional paths and context. When domain configuration is absent, derive review partitions and appropriate personas from the existing architecture and code without writing those docs. Keep a separate test-focused domain when the repo has a substantial test surface.

Create `code_review/` and an empty `code_review/non-issues.md` when absent. Ensure `/code_review/` is ignored in the target repository's `.gitignore`. Never stage, commit, or push review artifacts. If any are already tracked, report that ignore rules do not untrack them; leave the index unchanged unless the user authorizes untracking.

### 2. Review every domain

Invoking this skill authorizes parallel domain review and validation agents when available. Run one fresh reviewer per domain using its configured persona. With no delegation capability, perform the same complete passes sequentially. Each reviewer owns only its domain issue file. Keep shared `non-issues.md` edits with the coordinating agent; reviewers return proposed additions for reconciliation.

Read every file anchored by the domain thoroughly. Expand directory anchors to their relevant source, configuration, and test files. Follow immediate dependencies to validate behaviour. Read architecture, domain configuration, accepted non-issues, and the existing domain issue file for context.

Review categories — consider at least these:

1. Bugs — logic errors, runtime crashes, incorrect behaviour.
2. Security — auth bypasses, injection, data leaks, OWASP-style issues.
3. DRY / Code Reuse — duplicated logic, copy-paste code, missed abstractions.
4. Nits — style, naming, dead code, minor maintainability improvements.
5. Tests — missing coverage, stale tests, weak assertions, broken test structure.
6. UX — confusing flows, broken affordances, poor operator experience where relevant.

Exclude error handling. Silent substitution, dropped failures, lost causes, inconsistent error shapes, misplaced handling, over-broad catches, and hidden fallbacks or partial results belong to `improve-codebase-error-handling`. Do not report them here.

Require concrete evidence and consequence. Respect repo-local conventions and accepted product decisions. Keep reviewing after finding high-severity issues; retain all validated issues without a candidate quota. Do not duplicate existing valid findings or re-flag accepted non-issues unless their revisit trigger is met or code changed materially.

Write `code_review/{domain_slug}_issues.md`, updating the current file in place. Derive slugs from domain names: lowercase, replace `&` with `and`, replace other non-alphanumeric runs with underscores, trim surrounding underscores. Reuse established filenames when present.

Use this format for new issue files:

```md
# {Domain} — Code Review Issues

> Reviewed: YYYY-MM-DD

## Summary
{2-3 sentence overview of findings, patterns, and overall assessment}

## Critical
### C1. {Issue Title}
- [ ]
- **Category:** Bugs | Security | DRY / Code Reuse | Nits | Tests | UX
- **File:** `path/to/file:line_number`
- **Description:** {What is wrong, concrete trigger, evidence, and consequence}
- **Recommendation:** {Specific fix guidance}

## High
## Medium
## Low
## NIT
## Tests
```

Order findings by severity. Keep stable IDs for retained findings. Record domains with no validated findings and any files or areas that could not be reviewed. Reconcile cross-domain duplicates under the owning domain, retaining references where needed. Do not claim complete coverage when files remain unread.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the quality issue is concrete enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

### 3. Validate every issue and add fix guidance

Wait until all domain reviews finish. Run one fresh validation agent per domain issue file, using the same persona and separate context from its reviewer. Keep the same file ownership and shared-file reconciliation rules.

For every existing and newly found issue:

- Validate it fully in the current code before proposing a fix.
- Remove it if resolved, disproven, duplicated, or excluded error handling; retain the canonical finding for duplicates.
- Move explicitly accepted concerns into `code_review/non-issues.md` with a short reason and revisit trigger. Do not infer user acceptance from severity or implementation cost.
- For each still-valid issue, add or update **Industry Standard Fix:** with a concrete approach, affected code, relevant constraints, and verification. Explain the approach beyond a one-line suggestion.
- No shortcuts, hacks, or workarounds. Do not implement; the user will implement later.

Validate every issue, with no selection step or limit on findings. Reconcile non-issue additions centrally after each pass so subsequent runs see one consistent accepted-concern register.

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for quality.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the issue or flow after that concept instead of inventing a file-shaped name.

Finish with domain coverage, finding counts by severity, issue-file paths, accepted/resolved finding changes, and any verification limitations. Check the final diff for accidental implementation changes and confirm review artifacts remain uncommitted. Do not commit or push as part of this review workflow.
