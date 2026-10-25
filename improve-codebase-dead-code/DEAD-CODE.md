# Dead Code

How to remove dead code safely, given its reachability evidence and the invariants of live paths. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **element**, **entry point**, **live**, **reference**, **dynamic reference**, **dead closure**, **residue**.

## Dead-code categories

When assessing a candidate for removal, classify it. The category determines what should change and how the removal is verified.

### 1. Unreferenced element

A file, export, function, type, constant, or configuration key has no references outside its own definition and tests. Remove it and its dead closure. Apply the **reference** and **dynamic-reference** tests.

### 2. Impossible branch

A branch's condition can never be true on any live path, because of a constant, an exhausted type, or an upstream guarantee. Remove the branch and simplify the condition. Apply the **condition** test.

### 3. Settled flag

A flag is permanently on or off in every environment. Remove the flag and its dead branch, keeping the live branch. Exclude flags whose rollout is still a product decision. Apply the **flag** test.

### 4. Test-only element

An element is referenced only by tests. Remove the element and the tests that exist only to exercise it. Apply the **test-only** test.

### 5. Unwired entry point

A route, job, command, or handler is defined but never registered or scheduled. Remove it and its dead closure. Apply the **reachability** test.

### 6. Residue

An alias, shim, wrapper, or compatibility path has lost its last user. Remove it. Apply the **residue** test.

## Removal discipline

- **Keep the reachability trace concrete.** Apply the **reachability walkthrough** to a specific element and state which entry points and references were checked.
- **Rule out dynamic references before removal.** Static search alone does not prove an element dead.
- **Treat external consumers as entry points.** Exports of a published package, public API fields, and other interfaces consumed outside the repository are live unless external evidence shows otherwise.
- **Exclude undecided flags.** A flag whose rollout is still a product decision is not a candidate.
- **Remove the full dead closure.** Remove helpers, types, configuration, documentation, and tests that exist only for the removed element.
- **Keep removals proportional.** A dead-code candidate does not by itself justify restructuring live code.
- **Keep live behaviour unchanged.** Separate any proposed live-behaviour change from the removal.

## Verification strategy

- Record the reachability walkthrough before removal: entry points checked, static references found, and dynamic references ruled out.
- Run the dynamic-reference check: string lookups, registries, reflection, configuration, serialized names, and framework conventions.
- Remove the element and its dead closure.
- Preserve live behaviour through existing tests and the repository's correctness gate.
- Delete tests that only exercised removed elements. Keep tests that cover live behaviour.
- Avoid tests that assert an element's absence.
