# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "robustness," "resilience," or "error checking." Consistent language is the whole point.

## Terms

**Failure**
An operation's inability to produce its intended result. Deliberately scale-agnostic — applies equally to an I/O error, parse error, dependency failure, timeout, rejected input, or violated invariant.

**Failure path**
The route a failure takes from its origin to its observer, including every handler, conversion, and layer it crosses.

**Origin**
Where a failure first occurs. The origin holds the most specific knowledge of what went wrong.

**Observer**
Where a failure is finally seen and acted on: a calling module, a user, an operator, or a log that someone reads. A failure that reaches no observer has been dropped.

**Handler**
Code that catches, converts, wraps, logs, retries, or drops a failure. Each handler is a point where a failure path can lose explicitness, cause, or shape.

**Owning layer**
The layer with the context to decide how a failure is handled: retry it, translate it, report it, or stop. Layers below lack the context; layers above inherit a decision already made.

**Error shape**
The type, status, code, and payload a failure surfaces as. The same kind of failure should surface in the same shape everywhere in a domain.

**Cause**
The original error and the context in which it occurred. A cause is preserved when the observer, or whoever investigates, can recover it after every wrap, rethrow, and translation.

**Fallback**
A substitute result used in place of a failed operation. A fallback is part of the contract only when the observer can tell it was used.

**Invariant**
Behaviour that must remain unchanged by an error-handling change. Includes success-path results, ordering, isolation, transaction semantics, freshness, determinism, and other path-specific contracts.

**Verification**
Evidence that an injected failure reaches its observer explicitly, in the standard shape, with its cause, while invariants remain intact. The verification surface is what the observer receives.

## Principles

- **The failure walkthrough.** Trace a representative failure from origin to observer. Identify every point where it is caught, converted, wrapped, logged, or dropped, and what the observer finally receives.
- **The substitution test.** A failure must never become a value the observer cannot distinguish from success. Defaults, empty collections, zero, `None`, and stale values returned in place of a failure are candidates.
- **The cause test.** After every wrap, rethrow, or translation, the original error and its context must remain recoverable.
- **The shape test.** The same kind of failure should surface in the same type, status, code, and payload across a domain. Distinct kinds of failure should remain distinguishable.
- **The ownership test.** Handle a failure at the layer with the context to decide, and nowhere else. Lower layers propagate; higher layers receive the owning layer's decision.
- **The catch-scope test.** A handler should catch only the failures it actually handles. A broad catch that absorbs unrelated failures turns defects into silent behaviour.
- **The fallback test.** A fallback is valid only when it is part of the contract and the observer can tell it was used. An undeclared fallback is a silent failure.
- **The partial-result test.** When some units of a batch fail, the observer must be able to tell which failed and why. A partial result reported as complete is a silent failure.
- **Absence is not failure.** A legitimately empty or missing result and a failed operation must surface differently.
- **Verification matches the failure.** Inject the failure at its origin and assert what the observer receives: explicitness, shape, and cause. Then verify preserved invariants through the repository's correctness gate.

## Relationships

- A **Failure** begins at an **Origin** and travels a **Failure path** to an **Observer**.
- Each **Handler** on the path can preserve or lose explicitness, **Cause**, and **Error shape**.
- The **Owning layer** is the one **Handler** position where the handling decision belongs.
- A **Fallback** is legitimate only when the **Observer** can tell it was used.
- **Verification** shows that the **Observer** receives the failure explicitly, in the standard **Error shape**, with its **Cause**, and that the **Invariants** survived.

## Rejected framings

- **Error handling as more handlers**: adding catches without an owning layer increases the number of places a failure can be dropped.
- **Robustness as never failing**: a fallback that hides a failure trades a visible defect for wrong behaviour that looks correct.
- **Logging as handling**: a failure that is logged while the caller continues as if it succeeded is still dropped.
- **Consistency as one global error type**: shape consistency applies per kind of failure; collapsing distinct failures erases distinctions the observer needs.
