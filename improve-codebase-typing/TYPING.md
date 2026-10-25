# Typing

How to make a value flow's types true safely, given its entry, uses, and invariants. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **value flow**, **entry**, **declared type**, **runtime value**, **boundary**, **parse**, **escape**, **narrowing**.

## Defect categories

When assessing a candidate for typing, classify its defect. The category determines what should change and how the value flow is verified.

### 1. Unparsed boundary

Data from requests, files, environment, database rows, messages, or untyped library returns enters typed code through a cast or an assumed shape. Parse it at the boundary into a typed value or an explicit failure, and let downstream code rely on the parsed type. Apply the **boundary-parse** test.

### 2. Unchecked escape

`Any`, unchecked `unknown`, a cast, or a non-null assertion claims a type that no check establishes. Remove the escape and establish the type through a parse, narrowing, or a corrected declaration. Apply the **escape** and **truth** tests.

### 3. False narrowing

A type guard, assertion function, or conditional claims a refinement it does not check. Make the check real or remove the claim. Apply the **narrowing** test.

### 4. Wrong nullability

A value declared present can be absent, or a value declared optional is always present. Correct the declaration to match the runtime value and handle absence where it actually occurs. Apply the **nullability** test.

### 5. Imprecise type

A plain string, number, or dictionary stands in for a known union, literal set, enumeration, or structured record. State the known set of values in the declared type. Apply the **precision** test.

### 6. Propagated imprecision

An imprecise type at one source spreads through inference into many callers. Correct it at the source and let inference carry the precise type. Apply the **propagation** test.

### 7. Unjustified suppression

An ignore comment or checker suppression hides a real disagreement. Fix the disagreement and remove the suppression, or state why the checker is wrong. Apply the **suppression** test.

## Typing discipline

- **Keep the value flow concrete.** Apply the **type walkthrough** to a specific entry and its uses. State where the declared type and the runtime value can disagree.
- **Fix at the source.** Correct a type where it originates, not at each use.
- **Parse once at the boundary.** Establish the type where untrusted data enters. Downstream code relies on the parsed type instead of re-checking it.
- **Preserve ownership.** Improve types within the documented architecture. If the candidate requires changing domain ownership, introducing a seam, or concentrating distributed invariants, identify the architecture work explicitly.
- **Keep changes proportional.** A typing candidate does not by itself justify a new validation library, type framework, or repository-wide checker configuration change.
- **Keep valid-input behaviour unchanged.** Declare any rejection of previously accepted invalid input in the plan. Separate any other behaviour change from the typing change.

## Verification strategy

- Remove the escape and run the type checker on the affected value flow.
- For boundaries, test that invalid input is rejected with an explicit failure and valid input parses to the declared type.
- For nullability and narrowing, exercise the absent or unrefined runtime value through the existing interface.
- Assert through the boundary's or module's interface, not internals.
- Preserve behaviour through existing tests and the repository's correctness gate.
- Avoid tests that only restate what the type checker already proves or assert annotation text.
