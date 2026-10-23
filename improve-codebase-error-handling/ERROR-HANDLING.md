# Error Handling

How to improve a failure path safely, given its origin, observer, and invariants. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **failure**, **failure path**, **origin**, **observer**, **handler**, **owning layer**, **error shape**, **cause**, **fallback**.

## Defect categories

When assessing a candidate for error handling, classify its defect. The category determines what should change and how the failure path is verified.

### 1. Silent substitution

A handler returns a default, empty collection, zero, `None`, or stale value in place of a failure, and the observer cannot distinguish it from success. Remove the substitution and let the failure propagate to the owning layer, or make the outcome explicit in the result. Apply the **substitution** test.

### 2. Dropped failure

A failure is logged, counted, or ignored while the caller continues as if the operation succeeded. Surface the failure to its observer. Keep logging only where it accompanies, rather than replaces, propagation. Apply the **substitution** and **ownership** tests.

### 3. Lost cause

A rethrow, wrap, or translation discards the original error or its context. Chain the cause through every translation and carry the context the observer needs. Apply the **cause** test.

### 4. Inconsistent shape

The same kind of failure surfaces as different types, statuses, codes, or payloads, or distinct kinds collapse into one indistinguishable shape. Express each kind through the domain's established error shape and translate once at the seam where the shape changes. Apply the **shape** test.

### 5. Misplaced handling

A failure is handled below the layer with the context to decide, or the owning layer passes it through without deciding. Move the decision to the owning layer and remove handlers that pre-empt it. Apply the **ownership** test.

### 6. Over-broad catch

A handler catches more than it handles, absorbing unrelated failures and defects. Narrow the catch to the failures the handler actually handles and let the rest propagate. Apply the **catch-scope** test.

### 7. Hidden fallback or partial result

A retry, fallback, or partial batch result hides that an operation failed. Declare the fallback in the contract so the observer can tell it was used, or report which units failed and why. Apply the **fallback** and **partial-result** tests.

## Handling discipline

- **Keep the failure path concrete.** Apply the **failure walkthrough** to a specific origin and observer. State what the observer currently receives.
- **Distinguish absence from failure.** Preserve legitimately empty and missing results as explicit states. A fix must not turn a valid absence into a failure.
- **Preserve ownership.** Improve handling within the documented architecture. If the candidate requires changing domain ownership, introducing a seam, or concentrating distributed invariants, identify the architecture work explicitly.
- **Keep the claimed benefit precise.** Missing logs, metrics, and alerts without a dropped failure belong to observability. Reduced runtime cost belongs to performance. Keep the error-handling proposal focused on what the observer receives.
- **Keep changes proportional.** An error-handling candidate does not by itself justify a new error framework, global error type, result-type library, or retry infrastructure.
- **Keep success paths unchanged.** Separate any proposed success-path behaviour change from the error-handling change.

## Verification strategy

- Inject the failure at its origin through the real trigger or a test stand-in at an existing seam.
- Assert what the observer receives: an explicit failure, in the standard error shape, with its cause recoverable.
- For fallbacks and partial results, assert that the observer can tell the fallback was used or which units failed.
- Assert through the observer's interface, not handler internals.
- Preserve success-path behaviour through existing tests and the repository's correctness gate.
- Avoid tests that only assert a handler exists, a log line's wording, or an exception class name the observer never sees.
