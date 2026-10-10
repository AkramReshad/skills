---
name: improve-codebase-readability
description: "Find readability opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-readability or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Readability

Surface comprehension friction and propose **readability opportunities** — refactors that reduce the context a reader must retain to understand or safely change behaviour. The aim is local reasoning and maintainability.

## Glossary

Use these terms consistently when discussing readability. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Reading task** — a representative question a maintainer must answer about behaviour, such as which fallback wins, when a write occurs, or what a change would affect.
- **Cognitive load** — concepts, choices, context switches, and hidden facts a developer must hold to complete the task.
- **Local reasoning** — understanding a decision and its consequences from a small, coherent body of code and explicit contracts.
- **Responsibility** — a coherent purpose with its own rules and reasons to change.
- **State** — values and effects whose current meaning depends on the execution path so far.
- **Abstraction level** — the level of detail at which code describes intent, policy, orchestration, or mechanics.
- **Contract** — what a reader must know about an operation: inputs, results, effects, ordering, invariants, and error modes.
- **Invariant** — behaviour that must remain unchanged: results, ordering, isolation, transaction semantics, error modes, freshness, or determinism.
- **Verification** — evidence that the reading task became easier while behaviour and ownership remained intact.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **The change-context test**: "To change this decision safely, how much unrelated code must I understand?"
- **The reading walkthrough**: trace a representative question through the code. Identify what must be remembered, inferred, revisited, or opened elsewhere.
- **The extraction test**: a helper earns its place when its name and contract let the reader understand the caller without reconstructing the helper's implementation.
- **Verification matches the friction.** Explain which facts the reader no longer needs to retain and which rules become explicit.

Anchor each proposal in a concrete difficulty understanding existing behavior. Choose changes that directly reduce that difficulty. Keep structural changes proportional to the readability problem, and explain how they make the behavior easier to follow.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to behaviour and decisions, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`
- Relevant `notes/` for the repo or workspace

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one decision require retaining unrelated responsibilities or details?
- Where do branches interact across a function, so an earlier flag changes the meaning of later code?
- Where do variables change meaning, or several mutable values have to be tracked together?
- Where do fallback precedence, sequencing, or transaction rules exist only in execution order?
- Where does a workflow repeatedly switch between policy, orchestration, and low-level mechanics?
- Where do names, dense expressions, or hidden effects make behaviour difficult to explain?
- Where do helpers fragment one coherent operation and force the reader to reconstruct it across calls?

Apply the **change-context**, **reading-walkthrough**, **responsibility**, **state**, **ordering**, **abstraction-level**, **naming**, and **extraction** tests in [READABILITY.md](READABILITY.md). Require concrete friction in representative reading tasks; aesthetic preference alone is not a candidate. Trace relevant callers, helpers, and tests before attributing difficulty to the implementation. Function length and complexity metrics may guide exploration; each candidate must explain the actual comprehension burden.

### 2. Present candidates

Present a numbered list of readability opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Reading task** — which question a maintainer needs to answer or decision they need to change
- **Problem** — what must be remembered, inferred, revisited, or reconstructed to understand the behaviour
- **Evidence** — concrete branches, state changes, ordering dependencies, names, or call paths establishing the friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of local reasoning and reduced cognitive load
- **Verification** — how the same reading task and preserved invariants would be checked

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for readability.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the operation or decision after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the friction is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — representative reading task, responsibilities, state, ordering, contracts, invariants, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Naming an operation or decision after a domain concept not in `UBIQUITOUS_LANGUAGE.md`?** Add the term there only when it is meaningful to product/business/domain experts, preserve the existing table style, and update the last-updated date.
- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md` and `{repo}/docs/codebase_architecture.md` when the change affects those docs.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future readability reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative implementations for the chosen candidate?** See [READABILITY-DESIGN.md](READABILITY-DESIGN.md).
