---
name: improve-codebase-contracts
description: "Find contract-consistency opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-contracts or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Contracts

Surface contract drift and propose **contract-consistency opportunities** — changes that make every consumer of a boundary contract agree with its producer. The aim is agreement across language and process boundaries.

## Glossary

Use these terms consistently when discussing contracts. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Boundary contract** — a contract with a producer and consumers across a language or process boundary: an API and its client, an event and its handler, a schema and its ORM.
- **Producer** — the side that defines and emits the contract. Its definition is the source of truth.
- **Consumer** — a side that reads, parses, or depends on the contract.
- **Definition** — where a side declares the contract: a schema, model, type, parser, or serializer.
- **Drift** — any disagreement between the producer's definition or output and a consumer's definition.
- **Source of truth** — the single definition from which other definitions are generated or derived.
- **Runtime parse** — consumer-side validation of contract data at the boundary.
- **Invariant** — behaviour that must remain unchanged: producer output, results, ordering, error modes, and compatibility for consumers outside the change.
- **Verification** — evidence that each targeted consumer parses real producer output with its own schema or parser and agrees field by field, while invariants remain intact.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Contract trace**: read the producer's definition and every consumer's, and compare them field by field.
- **Source-of-truth test**: one definition, with the others generated or derived from it.
- **The producer is the source of truth.** Consumers are corrected to match.
- **Verification parses real producer output.** Parse producer output with the consumer's schema or parser and assert agreement.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to contracts and their fields, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does a consumer type, schema, or parser declare fields the producer does not emit, or omit fields it does?
- Where do field names, types, units, or formats differ between producer and consumer?
- Where do required and nullable fields disagree across the boundary?
- Where do enum or literal value sets differ between sides?
- Where do consumers parse error payloads in a shape the producer does not emit?
- Where is the same contract defined by hand on both sides instead of generated or derived from one definition?
- Where do consumers trust boundary data without parsing it at runtime?
- Where are deprecated or renamed fields handled on one side only?

Apply the **contract-trace**, **source-of-truth**, **field**, **optionality**, **enum**, **error-shape**, **runtime-parse**, **version**, and **unused-field** tests in [CONTRACTS.md](CONTRACTS.md). Require a concrete boundary contract with its producer and consumers; a naming preference or stylistic difference alone is not a candidate. Trace the producer's actual output, not only its declared type, before attributing drift to a consumer.

### 2. Present candidates

Present a numbered list of contract-consistency opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Boundary contract** — the producer, its consumers, and the boundary they cross
- **Problem** — where the consumer disagrees with the producer and what happens when it meets real output
- **Evidence** — concrete definitions, serializers, parsers, or payloads establishing the drift
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of agreement, a single source of truth, and runtime parsing
- **Verification** — how real producer output and preserved invariants would be checked

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for contracts.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the contract or field after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the contract drift is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — boundary contract, producer, consumers, source of truth, drift, compatibility, invariants, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Naming a contract or field after a domain concept not in `UBIQUITOUS_LANGUAGE.md`?** Add the term there only when it is meaningful to product/business/domain experts, preserve the existing table style, and update the last-updated date.
- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md` and `{repo}/docs/codebase_architecture.md` when the change affects those docs.
- **Establishing a durable contract rule, such as which definition is generated from which?** Record it only when the user accepts the contract and the repository has an appropriate durable location.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future contract reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative contract designs for the chosen boundary contract?** See [CONTRACTS-DESIGN.md](CONTRACTS-DESIGN.md).
