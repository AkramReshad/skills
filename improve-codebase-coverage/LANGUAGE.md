# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "test coverage," "more tests," or "code coverage." Consistent language is the whole point.

## Terms

**Contract**
A behaviour callers rely on. Deliberately scale-agnostic — applies equally to a function result, a database write, an emitted event, an ordering guarantee, an error mode, or an edge case.

**Caller**
Code, a user, or an operator that depends on a contract. A contract matters because a caller relies on it.

**Test surface**
The interface through which a test exercises a contract. The best test surface is the interface the contract's callers use.

**Gap**
A contract that no existing test would catch breaking. A gap may exist in code with full line coverage.

**Mutation**
A deliberate change that breaks one contract while leaving the rest of the code intact: a flipped condition, a dropped write, a swapped order, a removed error, a shifted boundary.

**Assertion**
The check a test makes about observable behaviour. An assertion is strong when a mutation of its contract makes it fail.

**Invariant**
Behaviour that must remain unchanged by coverage work. Coverage work adds and replaces tests; it does not change production behaviour.

**Verification**
Evidence that each new test passes on current code and fails when its contract is mutated. The verification surface is the test outcome under mutation.

## Principles

- **The contract walkthrough.** List a module's contracts from its interface and callers. Map each contract to the test that would fail if it broke.
- **The mutation test.** If this behaviour broke, which test would fail? If none would, the contract is a gap.
- **The caller-reliance test.** Prioritize contracts callers actually depend on. Behaviour no caller relies on is not a coverage priority.
- **The edge test.** Boundaries carry contracts: empty, maximum, missing, duplicate, time, and precision edges each need a test when callers can reach them.
- **The error-mode test.** A failure contract is a contract. Rejections, raised errors, and fallbacks callers rely on need tests.
- **The regression test.** A fixed defect needs a test that would have failed before the fix.
- **The assertion-strength test.** A test that executes code without an assertion its contract's mutation would break protects nothing.
- **The interface-surface test.** Test a contract through the interface its callers use. A test past the interface breaks on refactors and leaves the caller's contract unprotected.
- **Production behaviour is an invariant.** Coverage work characterizes current correct behaviour. Suspected defects are reported, not locked in by tests.
- **Verification matches the contract.** Run each new test on current code, where it must pass, then mutate its contract, where it must fail. Then verify preserved behaviour through the repository's correctness gate.

## Relationships

- A **Caller** relies on a **Contract**.
- A **Contract** is exercised through a **Test surface**.
- A **Gap** is a **Contract** whose **Mutation** passes every existing test.
- A strong **Assertion** fails under its contract's **Mutation**.
- **Verification** shows each new test passes on current code, fails under **Mutation**, and leaves production behaviour unchanged.

## Rejected framings

- **Coverage as a line percentage**: executing a line is not testing its contract.
- **More tests as better coverage**: a test that repeats an existing assertion catches no new mutation and adds maintenance.
- **Testing internals for completeness**: a test past the interface breaks on refactors and leaves the caller's contract unprotected.
- **Testing current behaviour unconditionally**: a test that locks in a defect protects the wrong contract.
