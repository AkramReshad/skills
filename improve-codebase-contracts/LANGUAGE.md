# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "type mismatch," "schema sync," or "API cleanup." Consistent language is the whole point.

## Terms

**Boundary contract**
A contract with a producer and consumers across a language or process boundary. Deliberately scale-agnostic — applies equally to an HTTP endpoint and its client, an event and its handler, a database schema and its ORM, a message and its queue consumer, or a file format and its reader.

**Producer**
The side that defines and emits the contract. The producer's definition and its actual output are the source of truth for every consumer.

**Consumer**
A side that reads, parses, or depends on the contract. A contract may have many consumers in different languages or processes.

**Definition**
Where a side declares the contract: a schema, model, type, parser, validator, or serializer. A side may have several definitions of the same contract.

**Drift**
Any disagreement between the producer's definition or output and a consumer's definition. Includes field names, types, units, formats, optionality, value sets, error payloads, and versions.

**Source of truth**
The single definition from which other definitions are generated or derived. Hand-maintained definitions on both sides of a boundary have no source of truth.

**Runtime parse**
Consumer-side validation of contract data at the boundary. A static type on boundary data is an assumption until the consumer parses it.

**Invariant**
Behaviour that must remain unchanged by a contract-consistency change. Includes producer output, results, ordering, error modes, and compatibility for consumers outside the change.

**Verification**
Evidence that each targeted consumer parses real producer output with its own schema or parser and agrees field by field. The verification surface is real producer output meeting the consumer's definition.

## Principles

- **The contract trace.** Read the producer's definition and its actual output, then every consumer's definition. Compare them field by field and record each disagreement.
- **The source-of-truth test.** One definition should exist, with the others generated or derived from it. Two hand-maintained definitions of one contract will drift.
- **The field test.** Field names, types, units, and formats should agree across the boundary.
- **The optionality test.** Required, optional, and nullable fields should agree. A consumer that requires a field the producer may omit fails on real output.
- **The enum test.** Enum and literal value sets should agree. A value the producer emits and the consumer rejects or ignores is drift.
- **The error-shape test.** Consumers should parse the error payloads the producer actually emits.
- **The runtime-parse test.** Consumers should validate boundary data at runtime instead of trusting a static type.
- **The version test.** Deprecated, renamed, and added fields should be handled on both sides.
- **The unused-field test.** A field produced but consumed nowhere, or consumed but never produced, is drift.
- **The producer is the source of truth.** Correct consumers to match the producer. A change to producer output is a behaviour change, not a consistency fix.
- **Verification parses real producer output.** Capture output through the producer's own serializer and parse it with the consumer's schema or parser. Then verify preserved invariants through the repository's correctness gate.

## Relationships

- A **Boundary contract** has one **Producer** and one or more **Consumers**.
- Each side expresses the contract through one or more **Definitions**.
- **Drift** is a disagreement between the producer's output or **Definition** and a consumer's **Definition**.
- A **Source of truth** prevents drift by deriving the other **Definitions** from one.
- A **Runtime parse** turns undetected drift into an explicit failure at the boundary.
- **Verification** shows that consumers agree with real producer output and that the **Invariants** survived.

## Rejected framings

- **Consistency as matching type names**: identical names with different optionality, value sets, or formats still drift.
- **The consumer as the source of truth**: changing producer output to fit one consumer breaks every other consumer.
- **Types as runtime guarantees**: a static type on boundary data is an assumption until the consumer parses it.
- **Shared fixtures as proof**: a hand-written fixture both sides accept can still disagree with what the producer emits.
