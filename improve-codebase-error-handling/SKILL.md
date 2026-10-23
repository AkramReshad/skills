---
name: improve-codebase-error-handling
description: "Find error-handling opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-error-handling or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Error Handling

Surface failure-handling friction and propose **error-handling opportunities** — changes that make every failure reach its observer explicitly, in a consistent shape, with its cause intact. The aim is explicit and consistent failure surfacing.

## Glossary

Use these terms consistently when discussing error handling. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Failure** — an operation's inability to produce its intended result: an I/O error, parse error, dependency failure, timeout, or invariant violation.
- **Failure path** — the route a failure takes from its origin to its observer.
- **Origin** — where a failure first occurs.
- **Observer** — where a failure is finally seen and acted on: a caller, user, operator, or log.
- **Handler** — code that catches, converts, wraps, logs, retries, or drops a failure.
- **Owning layer** — the layer with the context to decide how a failure is handled.
- **Error shape** — the type, status, code, and payload a failure surfaces as.
- **Cause** — the original error and the context in which it occurred.
- **Invariant** — behaviour that must remain unchanged: success-path results, ordering, isolation, transaction semantics, freshness, or determinism.
- **Verification** — evidence that the failure reaches its observer explicitly, in the standard shape, with its cause, while invariants remain intact.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Failure walkthrough**: trace a representative failure from origin to observer. Identify every point where it is caught, converted, wrapped, logged, or dropped.
- **Substitution test**: a failure must never become a value the observer cannot distinguish from success.
- **Ownership test**: handle a failure at the layer with the context to decide, and nowhere else.
- **Verification matches the failure.** Inject the failure and assert what the observer receives.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to failures and their outcomes, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does a handler return a default, empty collection, zero, `None`, or stale value that the observer cannot distinguish from success?
- Where is a failure logged and then discarded, so the caller continues as if the operation succeeded?
- Where do rethrows, wraps, or translations drop the original error or its context?
- Where does the same kind of failure surface as different types, statuses, codes, or payloads?
- Where do broad catches absorb failures the handler does not actually handle?
- Where is a failure handled below the layer with the context to decide, or passed through the layer that should decide?
- Where do retries, fallbacks, or partial results hide that an operation failed?
- Where do boundaries accept external input without surfacing parse or validation failures?

Apply the **failure-walkthrough**, **substitution**, **cause**, **shape**, **ownership**, **catch-scope**, **fallback**, and **partial-result** tests in [ERROR-HANDLING.md](ERROR-HANDLING.md). Require a concrete failure path from origin to observer; a missing handler or stylistic preference alone is not a candidate. Trace callers, handlers, and observers before attributing the defect to one location.

### 2. Present candidates

Present a numbered list of error-handling opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Failure path** — the origin, the handlers it passes through, and the observer
- **Problem** — what the observer receives instead of an explicit failure in the standard shape with its cause
- **Evidence** — concrete handlers, conversions, catches, or call paths establishing the defect
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of explicitness, cause preservation, shape consistency, and ownership
- **Verification** — how the injected failure and preserved invariants would be checked

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for error handling.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the failure or flow after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the failure-handling friction is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — failure path, origin, owning layer, error shape, cause preservation, invariants, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Naming a failure or error shape after a domain concept not in `UBIQUITOUS_LANGUAGE.md`?** Add the term there only when it is meaningful to product/business/domain experts, preserve the existing table style, and update the last-updated date.
- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md` and `{repo}/docs/codebase_architecture.md` when the change affects those docs.
- **Establishing a durable error contract, such as a standard error shape for a domain?** Record it only when the user accepts the contract and the repository has an appropriate durable location.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future error-handling reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative handling designs for the chosen failure path?** See [ERROR-HANDLING-DESIGN.md](ERROR-HANDLING-DESIGN.md).
