# Ergonomics

How to improve a codebase surface safely, given its representative task and friction. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **task**, **surface**, **friction**, **organization**, **convenience**, **canonical path**.

## Friction categories

When assessing a candidate for ergonomics, classify its friction. The category determines what should change and how the representative task is verified.

### 1. Organization

Code placement, grouping, naming, exports, or imports make the correct location unpredictable. Improve the organization around domain vocabulary and existing ownership. Migrate callers to one canonical location and remove obsolete paths.

### 2. Discoverability

The correct capability exists but cannot be found naturally from nearby code, domain terms, or established entry points. Improve names, placement, exports, or concise usage guidance so the canonical path is evident.

### 3. Ceremony

Common callers repeat setup, conversions, arguments, or sequencing that do not express their intent. Introduce convenience through a stable default, helper, builder, composition, or entry point, then migrate repeated callers.

### 4. Choice and workflow

The surface exposes irrelevant implementation choices or fragments one task across unnecessary steps and context switches. Make the common correct path direct while keeping meaningful domain choices explicit.

## Canonical-path discipline

- **One task, one canonical path.** Don't add a convenience beside equally endorsed alternatives. Migrate representative callers and remove obsolete paths.
- **Preserve meaningful choices.** Domain decisions, invariants, error modes, and materially different workflows remain explicit. Convenience should hide stable ceremony, not intent.
- **Preserve ownership.** Improve placement and usage within the documented architecture. If the candidate requires changing responsibility, introducing a seam, or concentrating distributed invariants, it is an architecture candidate.
- **Keep runtime cost separate.** If the primary benefit is fewer queries, less CPU, lower memory use, or shorter execution, it is a performance candidate.

## Verification strategy: simplify, don't layer

- Walk the same representative task before and after the change.
- Verify the targeted friction directly: plausible locations, imports, required steps, arguments, choices, context switches, or files touched should fall.
- Migrate representative callers to the canonical path and delete obsolete aliases, wrappers, helpers, exports, and documentation.
- Preserve behaviour through existing tests and the repository's correctness gate.
- Add tests when the convenience carries behaviour, defaults, ordering, or error modes. Do not add brittle tests that merely encode file layout, line count, or syntax.
- Prefer examples drawn from real callers over synthetic demonstrations that avoid the actual friction.
