# Readability

How to improve comprehension safely, given a representative reading task and its invariants. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **reading task**, **cognitive load**, **local reasoning**, **responsibility**, **state**, **contract**.

## Friction categories

When assessing a candidate for readability, classify its friction. The category determines what should change and how the representative reading task is verified.

### 1. Responsibilities and abstraction levels

The reader switches among unrelated rules or between high-level intent and low-level mechanics. Identify each coherent responsibility and the context it needs. Group related statements, name meaningful operations, or separate policy from mechanics where this reduces the context needed for each decision. Apply the **responsibility** and **abstraction-level** tests.

### 2. Branches and state

Earlier flags alter later behaviour, variables change meaning, or several partially built values must be tracked together. Trace the paths and value lifetimes. Prefer stable names, explicit results, and locally complete branches where these reduce interacting state. Preserve cleanup, exception handling, and transaction semantics when changing control flow. Apply the **state** test.

### 3. Ordering and effects

Fallback precedence emerges from repeated assignments, correctness depends on distant sequencing, or an apparently simple expression performs I/O or mutates shared state. Identify the rule and make its ownership and effects visible. Preserve evaluation order, short-circuiting, and when failures or writes occur. Apply the **ordering** test.

### 4. Names and expressions

Names obscure domain roles, or nested expressions make a rule difficult to explain. Use canonical domain vocabulary and meaningful intermediate values. Follow local idioms; assess whether the new wording makes a concrete decision easier to understand. Apply the **naming** test.

### 5. Fragmentation and indirection

Understanding one coherent operation requires visiting several helpers whose contracts expose little useful meaning. Trace what each call lets the reader forget. Inline or regroup fragments when this restores a coherent explanation. When extracting a helper, include the added arguments, contracts, and navigation in the same assessment. Apply the **extraction** test.

## Scope discipline

- **Keep the reading task concrete.** Apply the **change-context** and **reading-walkthrough** tests to a specific question or decision. State what must currently be remembered or reconstructed.
- **Preserve ownership.** Improve comprehension within the documented architecture. If the candidate requires changing domain ownership, introducing a seam, or concentrating distributed invariants, identify the architecture work explicitly.
- **Keep the claimed benefit precise.** File discovery and repeated caller ceremony belong to ergonomics. Reduced runtime cost belongs to performance. Demonstrated incorrect behaviour belongs to quality. Identify overlap when present and keep the readability proposal focused on comprehension.
- **Keep contracts proportional.** A readability candidate does not by itself justify a new public interface, framework, configuration surface, or generic abstraction.
- **Keep behaviour explicit.** Preserve necessary domain distinctions and explicit missing or unavailable states. Separate any proposed behaviour change from the readability refactor.

## Verification strategy

- Walk the same reading task before and after the change, including relevant callers and helpers.
- Explain which facts no longer need to be retained, which ordering rules become visible, or which implementation details can now be understood through a contract.
- Account for added navigation and contracts. A shorter caller is useful when the complete reading task becomes easier.
- Preserve behaviour through existing tests and the repository's correctness gate.
- Add targeted coverage when important precedence, ordering, effects, or error modes lack protection. Assert observable behaviour through the existing interface.
- Avoid tests that enforce function length, helper names, statement layout, or an extraction pattern.
- Report readability evidence and correctness evidence separately. Passing tests establishes preserved behaviour; the reading walkthrough establishes the comprehension improvement.
