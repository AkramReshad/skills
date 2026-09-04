# Optimizing

How to improve a cost center safely, given its evidence and invariants. Assumes the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **workload**, **cost**, **cost center**, **cost model**, **optimization**, **invariant**, **verification**.

## Evidence categories

When assessing a candidate, classify its evidence. The category determines what is needed before the candidate is surfaced and how it should later be verified.

### 1. Structural proof

The code establishes the mechanism directly: a query inside a row loop, quadratic iteration, repeated schema DDL, duplicate serialization, unbounded materialization, or independent I/O serialized on the critical path. Surface the candidate without requiring a benchmark.

### 2. Cost-model inference

The mechanism is clear and the cost multiplies by an observable workload dimension such as rows, requests, instruments, providers, tests, or builds. Surface the candidate with the inferred amplification or scaling model.

### 3. Operational signal

Existing logs, query counts, traces, durations, memory observations, or production metrics indicate a cost center. Use the signal as evidence and inspect the implementation for the causal mechanism.

### 4. Targeted measurement

A focused benchmark, profiler, query counter, allocation measurement, or controlled experiment confirms magnitude. Use targeted measurement when static evidence is ambiguous, candidates need ranking, or implementation acceptance requires it.

Discovery may rely on structural proof or cost-model inference. Do not run an entire workload merely to attach a number to an already-established mechanism.

## Optimization mechanisms

Classify the proposed change by the mechanism that reduces cost:

- **Algorithmic complexity** — reduce work growth as input cardinality increases.
- **Redundant computation** — eliminate or reuse equivalent work.
- **Database/query efficiency** — remove N+1 queries, batch operations, reduce scans, or improve query shape.
- **I/O and round trips** — reduce filesystem, network, database, or process crossings.
- **Lifecycle amortization** — move valid initialization or teardown to an appropriate lifetime.
- **Concurrency and scheduling** — shorten the critical path with bounded independent work.
- **Caching and reuse** — reuse stable results with explicit validity and invalidation.
- **Serialization and allocation** — reduce copies, encodings, materialization, and intermediate state.
- **Build/test pipeline** — avoid repeated work, improve incrementality, or scope verification appropriately.
- **Runtime resource use** — reduce CPU, memory, bandwidth, storage, or infrastructure consumption.

## Optimization discipline

- **Prefer the existing seam.** When an interface already hides the cost center, improve its implementation without expanding the interface.
- **Preserve invariants explicitly.** State results, ordering, isolation, transaction semantics, error modes, freshness, and determinism that must survive.
- **Change architecture only when the mechanism requires it.** A performance candidate does not by itself justify a new module, interface, cache, queue, worker, or dependency.
- **Count permanent complexity as cost.** State, invalidation, concurrency, batching, and operational machinery must earn their maintenance burden.
- **Keep the optimization proportional.** Optimize the cost center established by the evidence; do not broaden the change into unrelated cleanup.

## Verification strategy

Match verification to the mechanism:

- N+1 query removal: query count remains bounded as records increase.
- Algorithmic complexity: operation count or scaling behaviour improves as input grows.
- Repeated setup: setup/teardown invocation count falls; targeted or workload timing may confirm impact.
- Overfetching: rows, columns, bytes, or materialized objects fall.
- Serial I/O: bounded concurrency shortens the critical path without violating ordering or rate limits.
- Duplicate computation: invocation count falls or cache/reuse behaviour is observable.
- Excess allocation: peak memory, allocation count, copy count, or intermediate size falls.
- Build duplication: executed task count or rebuilt scope falls; build duration may confirm impact.
- Direct latency or throughput claim: use a repeatable workload and a statistic appropriate to its variance.

Always run the repository's correctness gate after implementation. Add a durable performance regression only when it is stable enough to carry the contract without introducing flaky timing assertions.
