# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "cleanup," "legacy code," or "unused stuff." Consistent language is the whole point.

## Terms

**Element**
A unit of code that can be removed. Deliberately scale-agnostic — applies equally to a file, export, function, branch, flag, route, job, or compatibility shim.

**Entry point**
Where execution enters the system: a route, scheduled job, command, event handler, public interface consumed outside the repository, or registry. Everything live is reachable from an entry point.

**Live**
Reachable from at least one entry point. Rarely executed code is still live.

**Reference**
A use of an element: an import, call, registration, configuration entry, or string lookup. A reference from the element's own definition or its own tests does not make it live.

**Dynamic reference**
A reference resolved at runtime rather than visible in static search: a string lookup, registry, reflection, configuration value, serialized name, or framework convention.

**Dead closure**
The element plus everything only it reaches, including helpers, types, configuration, documentation, and tests that exist only to exercise it.

**Residue**
Aliases, shims, wrappers, and compatibility paths whose last user is gone.

**Invariant**
Behaviour that must remain unchanged by a removal. Includes results, ordering, isolation, transaction semantics, error modes, freshness, determinism, and other contracts of every live path.

**Verification**
Evidence that removing the element changes no live behaviour. No entry point reaches it, no dynamic reference resolves to it, and the correctness gate stays green after removal.

## Principles

- **The reachability walkthrough.** Trace the element back from every live entry point. Identify every static and dynamic reference and whether any lies on a live path.
- **The removal test.** Delete the element. If no entry point loses behaviour and the gate stays green, it was dead.
- **The reference test.** An element with no references outside its own definition and tests is a candidate.
- **The condition test.** A branch whose condition can never be true on any live path is dead.
- **The flag test.** A flag permanently on or off in every environment makes one of its branches dead. A flag whose rollout is still a product decision is not a candidate.
- **The test-only test.** An element referenced only by tests is dead, along with the tests that exist only to exercise it.
- **The dynamic-reference test.** Rule out string lookups, registries, reflection, configuration, serialized names, and framework conventions before declaring an element dead.
- **The residue test.** Aliases, shims, wrappers, and compatibility paths with no remaining user are dead.
- **Live behaviour is an invariant.** A removal must not change the behaviour of any live path.
- **Verification matches the removal.** Remove the element and its dead closure, run the dynamic-reference check, then verify through the repository's correctness gate.

## Relationships

- An **Entry point** makes an **Element** **Live** through a chain of **References**.
- A **Dynamic reference** can make an element live without appearing in static search.
- A dead element carries a **Dead closure** that is removed with it.
- **Residue** is dead code left behind after its last user migrated.
- **Verification** shows that no entry point lost behaviour and the **Invariants** survived.

## Rejected framings

- **Dead code as unfamiliar code**: an element is dead because no live entry point reaches it, not because it looks old.
- **Low usage as dead**: rarely executed code is still live.
- **Static search as proof**: a missing import does not prove an element dead when dynamic references are possible.
- **Disabling as removal**: commented-out, skipped, or permanently disabled code is still dead code.
