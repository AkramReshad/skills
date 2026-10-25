# Contracts

How to bring a boundary contract into agreement safely, given its producer, consumers, and invariants. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **boundary contract**, **producer**, **consumer**, **definition**, **drift**, **source of truth**, **runtime parse**.

## Drift categories

When assessing a candidate for contract consistency, classify its drift. The category determines what should change and how the boundary contract is verified.

### 1. Field drift

Field names, types, units, or formats differ between producer and consumer. Correct the consumer definition to match the producer's definition and actual output. Apply the **field** test.

### 2. Optionality drift

Required, optional, and nullable fields disagree, so real output fails or is misread at the consumer. Correct the consumer's optionality to match what the producer can emit. Apply the **optionality** test.

### 3. Value-set drift

Enum or literal value sets differ, so the consumer rejects, ignores, or mislabels values the producer emits. Correct the consumer's value set to match the producer. Apply the **enum** test.

### 4. Error-shape drift

Consumers parse error payloads in a shape the producer does not emit. Correct consumer error parsing to the producer's actual error payloads. Apply the **error-shape** test.

### 5. Duplicated definition

The same contract is defined by hand on both sides with no source of truth. Derive consumer definitions from the producer's definition using the repository's established tooling, and remove the hand-maintained copies. Apply the **source-of-truth** test.

### 6. Unparsed boundary

A consumer trusts boundary data through a static type or cast without validating it at runtime. Parse at the boundary against the corrected definition. Apply the **runtime-parse** test.

### 7. Version drift

Deprecated, renamed, or added fields are handled on one side only. Bring the consumer in line with the producer's current version. Apply the **version** test.

### 8. Unused fields

A field is produced but consumed nowhere, or consumed but never produced. Remove the consumer's reliance on fields the producer never emits; record produced-but-unconsumed fields as evidence without changing producer output. Apply the **unused-field** test.

## Contract discipline

- **Keep the boundary contract concrete.** Apply the **contract trace** to a specific producer and its consumers. State where each consumer disagrees with real output.
- **Correct the consumer.** The producer's definition and output are the source of truth. If a candidate requires changing producer output, identify that behaviour change explicitly and keep it separate.
- **Preserve ownership.** Improve agreement within the documented architecture. If the candidate requires changing domain ownership, introducing a seam, or concentrating distributed invariants, identify the architecture work explicitly.
- **Keep the claimed benefit precise.** Keep the proposal focused on agreement between producer and consumers.
- **Keep changes proportional.** A contract-consistency candidate does not by itself justify a new code generator, schema registry, or contract framework. Derive definitions with the repository's established tooling.
- **Keep producer output unchanged.** Separate any proposed producer behaviour change from the contract-consistency change.

## Verification strategy

- Capture real producer output through the producer's own serializer, handler, or a recorded response at an existing seam.
- Parse it with the consumer's schema or parser and assert field-by-field agreement.
- Cover required, optional, and nullable fields, every emitted enum value, and the error payloads the producer emits.
- Where one definition derives the others, regenerate the derived definitions and assert they match the committed ones.
- Preserve producer behaviour through existing tests and the repository's correctness gate.
- Avoid tests that compare hand-written fixtures on both sides; a fixture both sides accept can still disagree with the producer.
