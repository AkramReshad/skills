---
name: improve-codebase-typing
description: "Find typing opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-typing or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Typing

Surface typing friction and propose **typing opportunities** — changes that make declared types match what values can actually be at runtime. The aim is types that state what is true.

## Glossary

Use these terms consistently when discussing typing. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Value flow** — the route a value takes from where it enters to where it is used.
- **Entry** — where a value enters typed code: external input, a parse, a library return, or an untyped module.
- **Declared type** — the type the code states for a value.
- **Runtime value** — what a value can actually be when the code runs.
- **Boundary** — where untrusted or untyped data enters typed code.
- **Parse** — runtime validation that turns untrusted data into a typed value or an explicit failure.
- **Escape** — a construct that turns checking off: `Any`, unchecked `unknown`, casts, non-null assertions, or ignore comments.
- **Narrowing** — a checked refinement of a type through control flow, a type guard, or a parse.
- **Invariant** — behaviour that must remain unchanged: results, ordering, isolation, transaction semantics, error modes, freshness, or determinism.
- **Verification** — evidence that declared types match runtime values: the type checker establishes them without the escape, and boundaries reject invalid input, while invariants remain intact.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Type walkthrough**: trace a value from its entry to its uses. Compare the declared type at each step with what the runtime value can be.
- **Truth test**: a declared type is wrong when a runtime value can violate it.
- **Boundary-parse test**: data entering typed code is parsed at the boundary, not cast.
- **Verification matches the escape.** Remove the escape, let the type checker establish the type, and test invalid input at the boundary.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to values and their types, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where do `Any`, unchecked `unknown`, untyped dictionaries, or raw JSON flow through code that treats them as known shapes?
- Where do casts, non-null assertions, or type conversions claim a type that no check establishes?
- Where does external data — requests, files, environment, database rows, library returns — enter without runtime parsing?
- Where are optional values treated as present, or always-present values declared optional?
- Where do plain strings, numbers, or dictionaries stand in for a known union, literal set, or structured type?
- Where does an imprecise type from one module spread through inference into its callers?
- Where do ignore comments or suppressions hide disagreements the checker would otherwise report?
- Where do type guards or assertions claim a narrowing they do not check?

Apply the **type-walkthrough**, **truth**, **boundary-parse**, **escape**, **narrowing**, **nullability**, **precision**, **propagation**, and **suppression** tests in [TYPING.md](TYPING.md). Require a concrete value flow where the declared type can disagree with the runtime value; checker strictness preference alone is not a candidate. Trace entries, conversions, and uses before attributing the defect to one location.

### 2. Present candidates

Present a numbered list of typing opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Value flow** — the entry, the conversions it passes through, and its uses
- **Problem** — where the declared type and the runtime value can disagree
- **Evidence** — concrete escapes, casts, unparsed boundaries, or inference paths establishing the defect
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of type truth, boundary parsing, and checker coverage
- **Verification** — how the type checker and boundary parse tests would establish the declared types and preserved invariants

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for typing.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the type or value after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the typing friction is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — value flow, entry, boundary parse, declared types, escapes, invariants, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Naming a type after a domain concept not in `UBIQUITOUS_LANGUAGE.md`?** Add the term there only when it is meaningful to product/business/domain experts, preserve the existing table style, and update the last-updated date.
- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md` and `{repo}/docs/codebase_architecture.md` when the change affects those docs.
- **Establishing a durable typing contract, such as checker strictness for a module?** Record it only when the user accepts the contract and the repository has an appropriate durable location.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future typing reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative typing designs for the chosen value flow?** See [TYPING-DESIGN.md](TYPING-DESIGN.md).
