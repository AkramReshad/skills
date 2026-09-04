---
name: improve-codebase-ergonomics
description: Find ergonomics opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use when the user wants to improve code organization, discoverability, developer convenience, or the effort required to understand and correctly use the codebase.
---

# Improve Codebase Ergonomics

Surface ergonomic friction and propose **ergonomics opportunities** — refactors that make representative developer tasks easier to find, understand, and perform correctly. The aim is organization and convenience.

## Glossary

Use these terms consistently when discussing ergonomics. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Task** — a representative developer action in the codebase, such as finding an implementation, adding a caller, constructing test state, changing configuration, or invoking a common operation.
- **Surface** — everything a developer must find, understand, choose, and do to complete a task correctly.
- **Friction** — effort imposed by the surface beyond the task's essential complexity.
- **Organization** — placement, grouping, naming, and import structure that makes code predictable to find and change.
- **Convenience** — useful defaults, helpers, composition, or entry points that reduce repeated ceremony for common tasks.
- **Ceremony** — required steps, arguments, imports, or setup that do not express the developer's intent.
- **Discoverability** — how readily the correct code or usage path can be found from the task and domain vocabulary.
- **Cognitive load** — concepts, choices, context switches, and hidden facts a developer must hold to complete the task.
- **Canonical path** — the single expected location or usage path for a task.
- **Verification** — evidence that the task became easier while behaviour and ownership remained intact.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Task walkthrough**: trace a representative task from intent to completion. Count what must be found, learned, chosen, and repeated.
- **Canonical-path test**: a developer starting from domain vocabulary should encounter one obvious location or usage path.
- **Ceremony test**: repeated steps that do not express intent should be removed, defaulted, composed, or hidden when the correct behaviour is stable.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to predictable organization and usage, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`
- `{repo}/CONVENTIONS.md` when present
- Relevant `notes/` for the repo or workspace

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does finding one concept require bouncing between surprising locations or unrelated names?
- Where do multiple files, exports, or import paths appear equally canonical?
- Where do common tasks require repeated setup, arguments, conversions, or sequencing that do not express intent?
- Where are callers forced to understand or choose details irrelevant to the common task?
- Where do helpers, fixtures, builders, commands, or configuration surfaces make correct usage hard to discover?
- Which routine changes require unnecessary context switches or edits across unrelated files?

Apply the **task walkthrough**, **canonical-path**, **organization**, **discoverability**, **ceremony**, **choice**, **common-path**, and **residue** tests in [ERGONOMICS.md](ERGONOMICS.md). Require concrete friction in representative tasks; aesthetic preference alone is not a candidate.

### 2. Present candidates

Present a numbered list of ergonomics opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Task** — which representative developer action pays the friction
- **Problem** — why the current organization or usage surface causes friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of organization, convenience, discoverability, ceremony, and cognitive load
- **Verification** — how task simplification and preserved behaviour would be checked

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for ergonomics.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the location or usage path after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the friction is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose detailed organization or usage designs yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — representative tasks, constraints, current organization or usage, the canonical path, convenience, what behaviour and ownership survive.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Naming a canonical location or usage path after a domain concept not in `UBIQUITOUS_LANGUAGE.md`?** Add the term there only when it is meaningful to product/business/domain experts, preserve the existing table style, and update the last-updated date.
- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behaviour?** Update `{repo}/docs/codebase_domains.md`, `{repo}/docs/codebase_architecture.md`, and `{repo}/CONVENTIONS.md` when the change affects those docs.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future ergonomics reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative organization or usage designs for the chosen candidate?** See [ERGONOMIC-DESIGN.md](ERGONOMIC-DESIGN.md).
