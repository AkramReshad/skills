# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "type safety," "strictness," or "type hygiene." Consistent language is the whole point.

## Terms

**Value flow**
The route a value takes from where it enters to where it is used, including every conversion, inference step, and module it crosses. Deliberately scale-agnostic — applies equally to a function argument, request payload, database row, configuration value, or library return.

**Entry**
Where a value enters typed code: external input, deserialization, a library return, or a call from an untyped module. The entry is where the declared type is first claimed.

**Declared type**
The type the code states for a value, through annotations, signatures, inference, or casts.

**Runtime value**
What a value can actually be when the code runs. A declared type is true when every possible runtime value satisfies it.

**Boundary**
Where untrusted or untyped data enters typed code: requests, files, environment, database rows, message payloads, and untyped library returns.

**Parse**
Runtime validation that turns untrusted data into a typed value or an explicit failure. A parse establishes the declared type; a cast only claims it.

**Escape**
A construct that turns checking off: `Any`, unchecked `unknown`, casts, non-null assertions, and ignore comments. Each escape is a point where the declared type can stop matching the runtime value without the checker noticing.

**Narrowing**
A checked refinement of a type through control flow, a type guard that performs the check it claims, or a parse.

**Invariant**
Behaviour that must remain unchanged by a typing change. Includes results, ordering, isolation, transaction semantics, error modes, freshness, determinism, and other flow-specific contracts. Boundary parsing changes behaviour for invalid input; that change belongs in the accepted plan.

**Verification**
Evidence that declared types match runtime values while invariants remain intact. The verification surface is the type checker establishing the type without the escape, plus boundary tests that reject invalid input and accept valid input.

## Principles

- **The type walkthrough.** Trace a value from its entry to its uses. Compare the declared type at each step with what the runtime value can be, and identify where checking is turned off.
- **The truth test.** A declared type is wrong when a runtime value can violate it. Find the input, path, or library behaviour that produces the violating value.
- **The boundary-parse test.** Data entering typed code is parsed at the boundary into a typed value or an explicit failure. A cast at a boundary is a candidate.
- **The escape test.** Each `Any`, unchecked `unknown`, cast, non-null assertion, and ignore comment turns checking off. An escape is a candidate unless a check establishes what it claims.
- **The narrowing test.** Refine types through checks the checker can see. An assertion or guard that claims a refinement without performing it is a candidate.
- **The nullability test.** A value declared present must never be absent. A value declared optional should be one that can actually be absent.
- **The precision test.** When the set of runtime values is known — a union, literal set, enumeration, or structured record — the declared type should state it.
- **The propagation test.** An imprecise type spreads through inference to every caller. Correct it where it originates.
- **The suppression test.** An ignore comment is valid only when the checker is wrong and the comment states why. A suppression hiding a real disagreement is a candidate.
- **Valid-input behaviour is an invariant.** A typing change states truths about values. It must preserve behaviour for valid input; any rejection of previously accepted invalid input belongs in the accepted plan.
- **Verification matches the escape.** Remove the escape, let the type checker establish the type, and test invalid and valid input at the boundary. Then verify preserved behaviour through the repository's correctness gate.

## Relationships

- A **Value flow** begins at an **Entry** and ends at its uses.
- A **Declared type** is true when every **Runtime value** satisfies it.
- A **Boundary** is an **Entry** for untrusted or untyped data; a **Parse** establishes the declared type there.
- Each **Escape** lets the **Declared type** and **Runtime value** disagree unnoticed.
- **Narrowing** refines a declared type through a check the checker can see.
- **Verification** shows that the declared types are established without the escapes and that the **Invariants** survived.

## Rejected framings

- **Typing as more annotations**: an annotation that restates `Any` or relies on a cast adds no truth.
- **Strictness as the goal**: a stricter checker setting is useful only where it exposes real disagreements between declared types and runtime values.
- **Casting as fixing**: a cast silences the checker without establishing the type.
- **Precision as new domain modelling**: precision states the set of values that already occur. Inventing new domain concepts is a design decision.
