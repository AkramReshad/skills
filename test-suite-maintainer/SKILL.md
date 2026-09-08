---
name: test-suite-maintainer
description: Aggressively audit and prune automated test suites while preserving distinct, meaningful regression protection. Use when asked to reduce test volume, delete low-value tests, consolidate redundant coverage, or perform a test-suite audit. Do not use to create new tests or change production code.
---

# Test Suite Maintainer

Reduce the suite to the smallest set that still protects meaningful product behavior. Perform one exhaustive review rather than waiting for repeated prompts to inspect overlooked categories.

## Governing Standard

A test earns its place only when it protects a distinct, meaningful behavior or failure mode that is not already protected by a stronger retained test.

Keep a test only when all applicable statements hold:

- It has a concrete behavioral contract.
- A plausible production defect would make it fail.
- Its assertions distinguish correct from incorrect behavior.
- Its contract is not already covered at an equal or stronger boundary.
- Its maintenance and execution cost is proportionate to the risk protected.

Aggressive means exhaustive and decisive. It does not mean optimizing for a deletion quota or coverage percentage.

The burden of proof belongs to retention. Uncertainty is a reason to inspect the production contract and retained suite more deeply, not an automatic reason to keep a test. Every survivor must have affirmative retention evidence.

A plausible mutation is insufficient when its impact is trivial or its introduction is unrealistic. The rejected defect must materially change user-visible behavior, a domain decision, persisted state, a public integration contract, or an operational guarantee that the product actually relies on.

## Scope

Audit, consolidate, prune, and delete tests, parameter rows, fixtures, factories, helpers, and test-only support code made dead by the pruning.

Do not:

- add replacement tests
- modify production code
- broaden the task into implementation or architecture work
- commit or push unless the user explicitly requests it

If the review reveals important untested behavior, report it separately; do not expand this skill into test creation.

## Establish the Baseline

1. Read repository instructions, test configuration, relevant domain documentation, and the production boundaries represented by the suite.
2. Record collected test count, test files, runtime, and coverage when the repository supports them.
3. Save the complete collected node-ID manifest. Inventory tests by domain and layer: unit, service, repository, provider or adapter, API or contract, integration, migration, tooling, and meta-policy.
4. Inspect existing uncommitted changes and preserve unrelated work.
5. Inventory test-like files excluded from normal collection. Delete them unless an explicit repository command executes them and they independently earn retention.

Use repository-native collection and test commands. Treat coverage as a regression signal, not the objective.

## One-Pass Exhaustive Review

Review the entire in-scope suite through every lens below before declaring the audit complete:

1. Duplicate contracts across files and layers.
2. Repeated provider, adapter, repository, and endpoint behavior already guaranteed by shared implementations.
3. Implementation-coupled assertions: private calls, mock choreography, internal ordering, and source structure.
4. Weak assertions that prove execution without proving correctness.
5. Parameter rows and examples that exercise the same semantic class.
6. Trivial language, framework, type-system, schema, or library guarantees.
7. Tests of constants, accessors, declarations, simple delegation, and configuration with no owned behavior.
8. Tests of fixtures, factories, mocks, support utilities, scripts, and test infrastructure rather than shipped behavior.
9. Static-policy and source-text tests better enforced by formatters, linters, type checkers, schema tools, or CI configuration.
10. Obsolete compatibility cases, unreachable states, and historical behavior no longer in the contract.
11. Expensive tests whose protected risk is already covered more cheaply and precisely.
12. Whole files left without unique behavioral value.

## Required Delegation

A comprehensive suite audit must use subagents when the environment provides them. The invoking agent is the coordinator and must not substitute its own solo review for delegation.

1. Inventory every in-scope test file before assigning work.
2. For a substantial suite, use 5–10 subagents when that capacity is available. Choose enough reviewers to keep partitions coherent and balanced; never spawn more than 10 for this workflow. Assign primary reviewers to non-overlapping domain partitions and reserve some capacity for cross-domain duplication, parameterization, implementation coupling, test infrastructure, static-policy tests, and expensive-test redundancy.
3. Give every reviewer this skill, its exact file scope or review lens, the collected node IDs in scope, and the relevant production context. Require classification of every assigned node as retain or delete, exact deletion rationales, retained equivalents, affirmative retention evidence, and edits within its assigned test-only scope.
4. Track assignment coverage by node ID. Every collected test must receive a primary classification; material or high-risk domains must receive an independent second lens. A review that lists only deletion candidates is incomplete.
5. Reconcile concurrent edits centrally and reject production-code changes or additions of replacement tests.
6. After the first wave, re-collect the surviving suite and partition the complete survivor node-ID manifest among fresh cross-domain and survivor-focused reviews. Reviewing a sample, disputed subset, or prior candidate list does not satisfy this step. Reuse completed subagents when concurrency slots are full.
7. Require at least one complete primary wave and one complete survivor wave. Continue additional internal waves within the same invocation until every survivor has affirmative retention evidence and an independent full-survivor review returns no further supported deletions. Do not wait for the user to ask for another pass.

If delegation is unavailable, state that a comprehensive audit cannot be validated under this skill and ask whether to proceed with a lower-confidence solo review. A dispute does not default to retention: adjudicate it against the full retention standard, and delete when the affirmative retention case remains incomplete.

## Deletion Evidence

Classify every deletion with one of these rationales:

- `duplicate`: name the stronger retained test or contract location.
- `redundant-layer`: identify the layer that owns and already verifies the behavior.
- `redundant-variant`: identify the shared semantic branch represented by another case.
- `implementation-coupled`: identify the internal detail whose change should not fail the suite.
- `weak`: state the plausible incorrect implementation that would still pass.
- `non-behavioral`: identify the external tool, framework, language, or declaration being retested.
- `obsolete`: identify evidence that the behavior is no longer supported.
- `test-infrastructure`: identify why the subject is not shipped behavior.

The evidence may remain in the work log unless the user requests a durable artifact. Do not create audit documents by default.

## Retention Evidence

Classify every surviving test or genuinely inseparable parameterized cluster with all of:

- `contract`: the observable behavior, invariant, or failure semantic it owns
- `mutation`: a plausible incorrect production change that this test rejects
- `owner`: why this architectural layer is the correct place to protect the contract
- `unique`: the search used to establish that no stronger retained test rejects the same mutation
- `cost`: why the risk protected justifies the test's setup, runtime, and maintenance surface

Delete tests whose retention case is merely that they exercise code, cover a line, use another input, document current behavior, might catch something, or appear useful. Consolidate a parameterized cluster when only some rows earn retention.

Tests for a production symbol used only by tests do not preserve a live product contract. Delete those tests and report the apparently dead production path separately without changing production code.

At the end of each wave, reconcile the node manifest exactly:

```text
original or wave-start nodes = retained nodes + deleted nodes
unclassified nodes = 0
```

Do not claim saturation without this accounting.

## Equivalence Rules

Treat tests as duplicates when they reject the same plausible production mutation, even when they differ in fixture values, names, files, routes, providers, or test level.

An equivalent need not assert the same intermediate fact. A retained downstream behavioral test is stronger when the same defect would necessarily change its observable result. Do not demand a one-to-one assertion match before deleting lower-level wiring coverage.

- One representative normally covers a semantic equivalence class. Multiple ordinary values through the same branch are one class.
- Zero, negative, empty, missing, null, stale, and unavailable inputs are separate only when the product contract or production behavior distinguishes them.
- Shared adapter or base-class behavior is tested once at the owning layer. Concrete implementations retain tests only for their own parsing, mapping, configuration, or failure semantics.
- Service behavior is not repeated through every API route. API tests retain validation, serialization, authentication, status, and error contracts introduced by the API boundary.
- Repository behavior is not repeated in service tests unless orchestration creates a distinct failure mode.
- Parser fixtures are retained per structurally distinct source format or failure class, not per field or sample payload.
- Configuration and defaults are retained only through meaningful runtime behavior, not snapshots of declarations.
- CLI and script tests retain user-visible command behavior. Source-text, import, launcher, and wiring checks do not qualify unless that exact artifact is the shipped contract.
- Exact messages, call order, call counts, and internal helper selection qualify only when externally contractual.

When choosing between equivalent tests, retain the one at the owning layer with the strongest behavioral assertion and lowest maintenance cost.

## Presumptive Pruning Rules

Apply these presumptions across the whole suite. Retain an exception only with complete retention evidence.

- **Thin wrappers and delegation:** delete branch-free tests that prove a collaborator was called and its result returned. Protect the owned behavior through the caller or integration boundary.
- **CLI and jobs:** retain core operation behavior and, when materially useful, one command-level parse/exit contract. Delete exhaustive parser, launcher, default forwarding, mock-call, and per-command wiring tests already covered below the CLI.
- **Catalogs, registries, configuration, and seeds:** delete snapshots that restate declarations, enumerate constants, or assert every mapping row. Retain only semantic validation rules and one meaningful runtime or persistence integration for the assembled configuration.
- **Providers and adapters:** retain source-specific parsing, normalization, and genuinely distinct source failures. Test shared transport, result wrapping, HTTP classification, URL construction, and adapter protocol behavior once at the owning abstraction rather than for every provider.
- **APIs:** retain serialization, validation, authentication, status, and error behavior introduced by the boundary. Delete route tests that merely repeat service results, especially repeated happy paths and entity variants.
- **Services and ingestion:** retain business decisions, transactionality, idempotency, replay, correction, partitioning, and material failure orchestration. Delete dispatch tables, simple forwarding, default propagation, and per-job repetitions of shared control behavior.
- **Repositories:** retain complex queries, conflict resolution, priority rules, transaction semantics, and persistence invariants. Delete simple CRUD forwarding and filter examples already exercised through a stronger behavior.
- **Migrations:** retain populated-data transformations, reversibility where supported, and invariants unavailable from the canonical schema. Delete empty-database smoke tests, revision bookkeeping, source-text checks, and schema facts already enforced mechanically.
- **Test infrastructure and policy:** delete tests of fixtures, factories, database reset helpers, test utilities, coverage scaffolding, source layout, workflow text, setup scripts, and static typing or file-size policy when standard tooling or CI owns the rule.
- **Parameterized suites:** keep one row per distinct product semantic. Collapse rows differing only by ordinary values, provider names, timestamps, enum members, or equivalent sides of the same production condition.

Rank survivors by collected-case count and test LOC after each wave. Re-review the largest clusters and any group with several tests against one production branch or declaration; these are common reservoirs of mechanical coverage.

## Selecting the Strongest Test

When several tests protect the same contract, retain the one that best combines:

- observable behavioral assertions
- representative inputs and realistic collaboration
- ownership at the correct architectural layer
- deterministic execution
- low setup and mocking complexity
- clear failure localization
- coverage of the broadest valid equivalence class without hiding distinct failures

Do not preserve duplicates merely because they use different fixtures, endpoints, providers, or values.

## High-Value Tests to Preserve

Require strong evidence before deleting tests that uniquely protect:

- domain calculations, business rules, and invariants
- public API and serialization contracts
- distinct boundary equivalence classes and meaningful failure mapping
- explicit missing, unavailable, partial, and stale-data semantics
- parsers against representative external payloads
- transactionality, concurrency, idempotency, ordering, and state transitions
- migrations and persistence behavior that static schema inspection cannot prove
- cross-component composition where individual components can pass while integration fails
- regressions tied to previously observed defects

Retention is based on unique protection, not category alone. A duplicate concurrency or parser test remains deletable when a stronger retained test rejects the same defect.

## Apply the Pruning

1. Apply all supported deletions from every review lens in the same audit run.
2. Prefer deleting redundant test cases and parameter rows before preserving artificial file symmetry.
3. Delete a whole file when no unique behavioral case remains.
4. Remove imports, fixtures, helpers, builders, and support modules made dead by the deletions.
5. Do not rewrite remaining tests except for minimal cleanup required by the pruning.
6. Re-collect the suite and inspect the resulting test inventory for missed duplicate clusters.
7. Reconcile every collected survivor against the retention-evidence ledger; delete unclassified or unsupported survivors.
8. Run the required complete delegated survivor review and apply any newly supported deletions.
9. Repeat collection, manifest reconciliation, and complete survivor review until deletion saturation is independently confirmed.

## Verification

Run, in order appropriate to the repository:

- test collection
- formatting checks
- lint and static analysis
- focused tests for affected domains
- the complete in-scope suite
- coverage comparison when available

A coverage decrease is expected when low-value tests are removed. It is diagnostic data, not evidence to restore tests and not a completion threshold. Restore a test only when inspection shows that the uncovered behavior independently satisfies the full retention standard.

Failures caused by dead test support code should be cleaned up. Do not change production behavior to accommodate the pruned suite. If the full suite cannot run, state the exact blocker and do not claim completion.

Review the final diff for accidental production changes, unrelated files, empty scaffolding, and residual dead test code.

Before completion, verify that the final collected count equals the retention ledger, all in-scope files appeared in the assignment record, and the final independent survivor wave classified every remaining node.

## Completion Report

Report:

- baseline and final collected test counts
- number and percentage removed
- files deleted or changed and net line change
- coverage before and after, when available
- exact verification commands and outcomes
- any high-risk areas intentionally retained after dispute
- whether changes are uncommitted, committed, or pushed

Do not report a reduction as successful merely because the count fell. Success is a materially smaller suite with preserved distinct regression protection and passing required gates.
