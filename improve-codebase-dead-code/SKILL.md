---
name: improve-codebase-dead-code
description: "Find dead-code opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use only when explicitly invoked as $improve-codebase-dead-code or by name. Do not invoke automatically for related codebase work."
---

# Improve Codebase Dead Code

Surface dead code and propose **dead-code opportunities** — removals of elements that no live entry point reaches. The aim is a codebase that contains only what it uses.

## Glossary

Use these terms consistently when discussing dead code. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Element** — a file, export, function, branch, flag, route, job, or compatibility shim.
- **Entry point** — where execution enters the system: a route, job, command, event handler, public interface consumed outside the repository, or registry.
- **Live** — reachable from at least one entry point.
- **Reference** — a use of an element: an import, call, registration, configuration entry, or string lookup.
- **Dynamic reference** — a reference resolved at runtime: a string lookup, registry, reflection, configuration value, serialized name, or framework convention.
- **Dead closure** — the element plus everything only it reaches, including tests that exist only to exercise it.
- **Residue** — aliases, shims, wrappers, and compatibility paths whose last user is gone.
- **Invariant** — behaviour that must remain unchanged: results, ordering, isolation, transaction semantics, error modes, freshness, or determinism of every live path.
- **Verification** — evidence that removing the element changes no live behaviour: no entry point reaches it, no dynamic reference resolves to it, and the correctness gate stays green.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Reachability walkthrough**: trace the element back from every live entry point. Identify every static and dynamic reference.
- **Removal test**: delete the element. If no entry point loses behaviour and the gate stays green, it was dead.
- **Dynamic-reference test**: before removal, rule out string lookups, registries, reflection, configuration, serialized names, and framework conventions.
- **Verification matches the removal.** Remove the element and its dead closure, then verify the gate and the dynamic-reference check.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to elements and entry points, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Which files, exports, or functions have no remaining importers or callers?
- Which branches depend on conditions that can never be true on any live path?
- Which flags are permanently on or off in every environment?
- Which elements are referenced only by their own tests?
- Which aliases, shims, wrappers, or compatibility paths have lost their last user?
- Which routes, jobs, commands, or handlers are defined but never registered or scheduled?
- Which configuration keys, constants, or types does nothing read?

Apply the **reachability**, **reference**, **condition**, **flag**, **test-only**, **dynamic-reference**, and **residue** tests in [DEAD-CODE.md](DEAD-CODE.md). Require a concrete reachability trace; unfamiliar code or low usage alone is not a candidate. Trace entry points, references, and dynamic lookups before declaring an element dead.

### 2. Present candidates

Present a numbered list of dead-code opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Element** — what would be removed and its dead closure
- **Problem** — why no live entry point reaches it
- **Evidence** — missing references, impossible conditions, settled flag values, and the dynamic-reference search
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of code no longer read, maintained, built, or tested
- **Verification** — how the removal and preserved live behaviour would be checked

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for dead code.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the element or flow after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the dead code is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — element, entry points, static and dynamic references, flags, dead closure, invariants, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md` and `{repo}/docs/codebase_architecture.md` when the change affects those docs.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future dead-code reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative removal designs for the chosen element?** See [DEAD-CODE-DESIGN.md](DEAD-CODE-DESIGN.md).
