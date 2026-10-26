---
name: improve-codebase-coverage
description: "Find coverage opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-coverage or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Coverage

Surface coverage gaps and propose **coverage opportunities** — tests that protect contracts callers rely on but no existing test would catch breaking. The aim is that every important contract fails a test when it breaks.

## Glossary

Use these terms consistently when discussing coverage. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Contract** — a behaviour callers rely on: results, effects, ordering, error modes, and edge cases.
- **Caller** — code, a user, or an operator that depends on a contract.
- **Test surface** — the interface through which a test exercises a contract.
- **Gap** — a contract that no existing test would catch breaking.
- **Mutation** — a deliberate change that breaks one contract while leaving the rest of the code intact.
- **Assertion** — the check a test makes about observable behaviour.
- **Invariant** — behaviour that must remain unchanged: coverage work does not change production behaviour.
- **Verification** — evidence that each new test passes on current code and fails when its contract is mutated.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Contract walkthrough**: list a module's contracts from its interface and callers, and map each contract to the test that would fail if it broke.
- **Mutation test**: if this behaviour broke, which test would fail? If none would, the contract is a gap.
- **Interface-surface test**: test a contract through the interface its callers use, not through internals.
- **Verification matches the contract.** A new test passes on current code and fails when its contract is mutated.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to contracts and behaviour, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Which behaviours do callers rely on that no test exercises?
- Where would a changed result, effect, or ordering pass every existing test?
- Which error modes, rejections, or fallbacks have no test?
- Which boundaries — empty, maximum, missing, duplicate, time, or precision edges — lack coverage?
- Which fixed defects have no regression test?
- Where do tests run code but make no assertion that could fail?
- Where do tests reach past the interface into internals, leaving the caller's contract untested?

Start from tool output. Inspect the repository for configured coverage and mutation testing and use them. If none exists, choose the best tools for the repository's languages and run them without adding them to the project's dependencies or configuration. Treat uncovered code and surviving mutants as candidates, not proof. Explore for what these tools cannot see: executed code whose behaviour no assertion checks, and contracts callers rely on across modules.

Apply the **contract-walkthrough**, **mutation**, **caller-reliance**, **edge**, **error-mode**, **regression**, **assertion-strength**, and **interface-surface** tests in [COVERAGE.md](COVERAGE.md). Require a concrete contract a caller relies on; a coverage percentage or an unexecuted line alone is not a candidate. Trace callers and existing tests before declaring a gap.

### 2. Present candidates

Present a numbered list of coverage opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Contract** — the behaviour callers rely on and the callers that rely on it
- **Problem** — which mutation of the contract would pass every existing test
- **Evidence** — concrete callers, existing tests, and the mutation that survives them
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of contracts protected and mutations caught
- **Verification** — how each new test would be shown to pass on current code and fail under mutation

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for coverage.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the contract or flow after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the coverage gap is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — contract, callers, test surface, edge cases, error modes, mutations, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Naming a contract after a domain concept not in `UBIQUITOUS_LANGUAGE.md`?** Add the term there only when it is meaningful to product/business/domain experts, preserve the existing table style, and update the last-updated date.
- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md` and `{repo}/docs/codebase_architecture.md` when the change affects those docs.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future coverage reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative test designs for the chosen contract?** See [COVERAGE-DESIGN.md](COVERAGE-DESIGN.md).
