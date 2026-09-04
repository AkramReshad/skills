# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "slow code," "hotspot," or "overhead." Consistent language is the whole point.

## Terms

**Workload**
A representative execution path whose cost matters. Deliberately scale-agnostic — applies equally to a function call, database query, request, ingestion run, test suite, build, or scheduled job.

**Cost**
A resource consumed by a workload. Includes latency, database or network round trips, CPU, memory, allocations, bytes transferred, process starts, and repeated setup. Wall time is one cost, not the definition of performance.

**Cost center**
The code or operation responsible for a meaningful share of a workload's cost. A cost center may be structurally evident before its exact share is measured.

**Cost model**
An explanation of how and why cost grows with workload size, execution frequency, or lifecycle. A cost model may be expressed through complexity, round-trip count, setup count, allocation volume, data movement, or measured time.

**Amplification**
Cost multiplied per row, request, instrument, provider, test, build, page render, or other repeated unit. Frequency is part of the cost model.

**Critical path**
The dependent operations that determine workload completion time. Independent work outside the critical path does not reduce completion time merely by becoming faster.

**Optimization**
An implementation change that reduces a workload's cost while preserving its invariants. The change may improve an algorithm behind an existing seam or alter execution structure when the accepted invariants permit it.

**Invariant**
Behaviour that must remain unchanged by an optimization. Includes results, ordering, isolation, transaction semantics, error modes, freshness, determinism, and other workload-specific contracts.

**Verification**
Evidence that an optimization reduced its targeted cost while preserving invariants. The verification surface must match the mechanism: query count for N+1 removal, operation count or scaling for algorithmic work, allocation volume for memory work, or timing when elapsed time is the direct claim.

## Principles

- **The amplification test.** Identify where cost multiplies. A small operation repeated across a high-cardinality workload can be the dominant cost center.
- **The scaling test.** Determine how cost changes as the workload grows. N+1 round trips, nested scans, repeated full-data passes, and lifecycle work repeated per execution are valid structural evidence.
- **The redundant-work test.** Equivalent work repeated within or across executions is a candidate when its result can be safely reused, shared, batched, or eliminated.
- **The lifecycle test.** Expensive setup scoped more narrowly than the state it initializes is a candidate for amortization when isolation and cleanup invariants can be preserved.
- **The round-trip test.** Database, filesystem, network, and process boundaries multiply fixed costs. Count crossings as part of the cost model.
- **The work-conservation test.** Work produced and discarded through overfetching, early materialization, filtering, copying, or unused variants is still cost paid by the workload.
- **The critical-path test.** Parallelism helps only when independent work lies on the critical path and concurrency costs remain bounded.
- **The reuse test.** Cache, pool, memoize, batch, or incrementally update only when validity and invalidation are explicit.
- **The resource-shape test.** Intermediate collections, copies, encodings, and allocations should be proportional to the useful result.
- **Measurements are one form of evidence.** Structural proof and a credible cost model are sufficient to surface a candidate. Measurements rank ambiguous candidates and verify implementation claims.
- **Verification matches the mechanism.** Use the narrowest reliable surface that proves the targeted cost fell and invariants survived.

## Relationships

- A **Workload** incurs one or more forms of **Cost**.
- A **Cost center** explains where a meaningful part of that **Cost** originates.
- A **Cost model** explains how the cost center scales or amplifies.
- An **Optimization** changes the cost center while preserving **Invariants**.
- **Verification** proves the targeted cost changed and the invariants remained true.
- **Amplification** and the **Critical path** determine whether a local cost center materially affects the workload.

## Rejected framings

- **Performance as wall time only**: misses query amplification, algorithmic scaling, memory, allocation, data movement, and infrastructure cost.
- **A benchmark as a discovery prerequisite**: misses structurally provable problems such as N+1 queries and quadratic iteration.
- **An inefficient-looking line as a candidate by itself**: code needs a representative workload, a credible cost model, and concrete evidence that the cost is paid.
- **Caching as a default optimization**: reuse is valid only when lifetime, validity, invalidation, and memory cost are explicit.
