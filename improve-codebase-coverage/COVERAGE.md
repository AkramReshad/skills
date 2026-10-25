# Coverage

How to close a coverage gap safely, given its contract and callers. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **contract**, **caller**, **test surface**, **gap**, **mutation**, **assertion**.

## Gap categories

When assessing a candidate for coverage, classify its gap. The category determines what test should be added and how it is verified.

### 1. Untested result

A result callers rely on can change without any test failing. Add an assertion on the result through the caller's interface. Apply the **mutation** and **caller-reliance** tests.

### 2. Untested effect or ordering

A write, call, emitted event, or sequencing guarantee callers rely on can be dropped or reordered without any test failing. Assert the observable effect or order through the interface or its existing test stand-ins. Apply the **mutation** test.

### 3. Untested edge

A boundary callers can reach — empty, maximum, missing, duplicate, time, or precision — has no test. Add cases for the reachable boundaries. Apply the **edge** test.

### 4. Untested error mode

A rejection, raised error, or fallback callers rely on has no test. Trigger the failure and assert what the caller receives. Apply the **error-mode** test.

### 5. Missing regression

A fixed defect has no test that would have failed before the fix. Add a test that reproduces the original trigger. Apply the **regression** test.

### 6. Weak assertion

A test exercises the contract but asserts nothing its mutation would break. Strengthen or replace the assertion. Apply the **assertion-strength** test.

### 7. Wrong test surface

A test reaches past the interface into internals, so the caller's contract stays unprotected. Replace it with a test through the caller's interface. Apply the **interface-surface** test.

## Coverage discipline

- **Keep the contract concrete.** Apply the **contract walkthrough** to a specific contract and its callers. State the mutation that currently survives.
- **Characterize correct behaviour.** If current behaviour appears defective, report it instead of locking it in with a test.
- **Change no production code.** If a contract cannot be tested through its current interface, report the testability problem instead of changing the interface.
- **One contract, one test home.** Add tests to the existing test module that owns the interface. Do not repeat an assertion an existing test already makes.
- **Keep changes proportional.** A coverage candidate does not by itself justify a new test framework, fixture system, or test infrastructure.

## Verification strategy

- Run each new test against current code; it must pass.
- Mutate the covered contract and confirm the new test fails; then restore the code.
- Assert observable behaviour through the caller's interface.
- Avoid assertions on internal calls, private state, log wording, or snapshots of output the contract does not define.
- Preserve production behaviour through existing tests and the repository's correctness gate.
