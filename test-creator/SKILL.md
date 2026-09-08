---
name: test-creator
description: Create, revise, and update high-signal automated tests for application behavior. Use when implementation work needs new regression coverage, existing tests must change with an intentional contract change, or a failing test needs correction. Do not use for suite-wide audits, pruning, or deletion campaigns; use test-suite-maintainer instead.
---

# Test Creator

Create the smallest set of tests that protects the changed behavior with clear failure signals and low maintenance cost.

## Priorities

1. Regression sensitivity. Each test must detect a plausible production defect.
2. Behavioral fidelity. Assert externally observable contracts, not incidental implementation.
3. Suite economy. Add no test whose protection already exists at an equal or stronger boundary.
4. Diagnostic clarity. A failure should identify the broken behavior without extensive investigation.

## Test-Worthiness Gate

Before adding a test, answer:

- What behavior, invariant, or failure mode does it protect?
- What plausible incorrect implementation would make it fail?
- Where is the same contract already tested?
- What is the lowest sufficient boundary for proving it?

Search nearby and domain-relevant tests before writing. If retained coverage already rejects the same defect, do not add another test. Do not create tests merely because a function, branch, file, or code change exists.

## Workflow

1. Read repository instructions, test configuration, the changed production code, and nearby tests.
2. Identify the changed observable contract and its meaningful equivalence classes.
3. Run or inspect existing focused tests to establish current coverage and conventions.
4. Add or revise only the cases needed to protect uncovered behavior.
5. Run the narrowest relevant tests while iterating.
6. Run the repository-prescribed test and static-analysis gates before handoff.

Do not start a suite-wide audit or delete unrelated tests. Do not commit or push unless the user explicitly requests it.

## Choosing the Boundary

Use the cheapest level that can prove the contract:

- Pure unit test for calculations, transformations, and domain rules.
- Service test for orchestration and business decisions across collaborators.
- Repository test for persistence queries, transactions, and database semantics.
- API or contract test for validation, serialization, status, and public error behavior.
- Integration test only when composition with a real boundary is the risk.

Keep a contract primarily at the layer that owns it. Add coverage at another layer only when that layer introduces a distinct failure mode.

## Assertions

Assert exact observable outcomes: return values, errors, persisted state, emitted events, or contractual dependency interactions. Multiple assertions are appropriate when they describe one coherent outcome.

Avoid assertions that only prove execution, including:

- the result is non-null or a collection is nonempty when exact content matters
- a mock was called when its arguments or effect carry the contract
- the response is one of several outcomes
- the source contains a string or declaration
- an object has the same values supplied by the test

A valid internal refactor should not break the test unless the refactored mechanism is itself part of the contract.

## Cases and Parameterization

Partition inputs by semantic behavior. Use one representative per equivalence class plus true boundaries.

Each parameter row must exercise a distinct rule, branch, boundary class, or failure mode. Different values traversing the same logic do not justify additional rows. Prefer a small explicit test when parameterization obscures why cases differ.

Cover negative paths when they express meaningful product behavior, data semantics, or recovery policy. Do not enumerate impossible states without evidence that the system owns their handling.

## Dependencies and Fixtures

Mock nondeterministic or external boundaries such as networks, clocks, subprocesses, and remote services. Prefer real domain objects and internal collaborators when they remain fast and deterministic.

Assert calls, call counts, and ordering only when the interaction is contractual. Avoid mocks whose setup duplicates the implementation algorithm.

Keep fixtures local, minimal, and explicit about fields relevant to the behavior. Use shared builders when they remove irrelevant construction noise without hiding important state. Avoid sleeps, ambient time, uncontrolled randomness, live network access, and order dependence.

## Do Not Create

- Tests of language, framework, compiler, type-checker, or schema-validator guarantees.
- Tests for trivial accessors, constant assignment, declarative mappings, or simple delegation without added behavior.
- Tests that inspect source layout, imports, annotations, filenames, or implementation structure when a standard static tool can enforce the rule.
- Tests of mocks, fixtures, factories, or test helpers unless those artifacts are shipped product functionality.
- Broad snapshots when focused semantic assertions are available.
- One test per production function as a mechanical completeness rule.
- New coverage solely to raise a percentage target.

## Revising Existing Tests

When an intentional product contract changes, update assertions to the new contract and preserve still-relevant regression coverage. When only implementation changes, repair tests that were coupled to internals rather than changing behavioral expectations.

Do not make a failing test pass by weakening it until it can no longer distinguish correct behavior. Confirm the production behavior before deciding that the test is wrong.

## Final Checks

For every added or materially revised test, confirm:

- it names and protects a distinct behavior or failure mode
- a plausible defect makes it fail
- existing tests do not already provide equivalent or stronger protection
- assertions target observable behavior with useful precision
- setup contains no irrelevant detail or excessive mocking
- parameter rows represent distinct semantics
- focused and required repository gates pass

Report the protected behaviors, tests changed, and exact verification commands.
