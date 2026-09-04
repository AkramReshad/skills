---
name: improve-codebase-performance
description: Find performance improvement opportunities in a codebase, informed by project domain language in UBIQUITOUS_LANGUAGE.md and repo architecture docs such as docs/codebase_domains.md and docs/codebase_architecture.md. Use when the user wants to improve latency, throughput, scalability, query or I/O efficiency, build or test speed, or resource use without needing to identify the bottleneck first.
---

# Improve Codebase Performance

Surface performance friction and propose **optimization opportunities** — implementation changes that reduce the cost of representative workloads while preserving behaviour. The aim is efficiency and scalability.

## Glossary

Use these terms consistently when discussing performance. Preserve repo-local and domain vocabulary where it is already canonical. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Workload** — a representative execution path whose cost matters, such as a request, query, ingestion run, test suite, build, or scheduled job.
- **Cost** — a resource consumed by a workload: latency, database or network round trips, CPU, memory, allocations, bytes, process starts, or repeated setup.
- **Cost center** — the code or operation responsible for a meaningful share of a workload's cost.
- **Cost model** — how and why cost grows with workload size, frequency, or lifecycle.
- **Amplification** — cost multiplied per row, request, instrument, provider, test, build, or other repeated unit.
- **Critical path** — the dependent operations that determine workload completion time.
- **Optimization** — an implementation change that reduces cost while preserving the workload's invariants.
- **Invariant** — behaviour that must remain unchanged: results, ordering, isolation, transaction semantics, error modes, freshness, or determinism.
- **Verification** — evidence that the optimization reduced its targeted cost while preserving invariants.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Amplification test**: identify where cost multiplies. A small cost repeated per row, request, or test can dominate the workload.
- **Scaling test**: determine how cost changes as the workload grows. Structural evidence such as N+1 queries or quadratic iteration is sufficient to surface a candidate.
- **Measurements are one form of evidence.** Concrete code structure and a credible cost model can establish a performance problem before a benchmark exists.
- **Verification matches the mechanism.** Query count, operation count, allocation volume, setup frequency, throughput, or wall time may be the right surface.

This skill is _informed_ by the project's domain language and architecture docs. `UBIQUITOUS_LANGUAGE.md` gives names to workloads and data, while repo-local `docs/codebase_domains.md` and `docs/codebase_architecture.md` show the runtime shape and domain ownership.

## Process

### 1. Explore

Read existing documentation first:

- `UBIQUITOUS_LANGUAGE.md` at the workspace root
- `{repo}/docs/codebase_domains.md`
- `{repo}/docs/codebase_architecture.md`
- `{repo}/CONVENTIONS.md` when present
- Relevant `notes/` for the repo or workspace

If any of these files don't exist, proceed silently — don't flag their absence or suggest creating them upfront.

Then walk the codebase. Use subagents only when the user explicitly asks for parallel agent work. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does cost multiply per row, request, instrument, provider, test, build, or page render?
- Where do database, filesystem, network, or process round trips occur inside loops?
- Where does cost grow faster than the useful workload?
- Where is invariant work recomputed, reparsed, rebuilt, refetched, or reserialized?
- Where is expensive setup scoped more narrowly than the state it initializes?
- Where is work produced and then discarded through overfetching, filtering, copying, or unused variants?
- Where are independent operations serialized on the critical path?
- Which common paths create disproportionate allocations, intermediate collections, or data movement?

Apply the **amplification**, **scaling**, **redundant-work**, **lifecycle**, **round-trip**, **work-conservation**, **critical-path**, **reuse**, and **resource-shape** tests in [OPTIMIZING.md](OPTIMIZING.md). Do not wait for the user to name a bottleneck. Do not require a full workload run when static evidence establishes the mechanism. Use targeted measurements when evidence is ambiguous or candidates need ranking.

### 2. Present candidates

Present a numbered list of optimization opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Workload** — which execution path pays the cost
- **Problem** — the cost center, amplification or scaling mechanism, and why it matters
- **Evidence** — concrete code structure, cost model, operational signal, or targeted measurement
- **Solution** — plain English description of what would change
- **Benefits** — which cost would fall and how scaling or resource use would improve
- **Verification** — how the mechanism and preserved invariants would be checked

**Use `UBIQUITOUS_LANGUAGE.md` vocabulary for the domain, repo architecture docs for module/domain placement, and [LANGUAGE.md](LANGUAGE.md) vocabulary for performance.** If `UBIQUITOUS_LANGUAGE.md` defines a domain concept, name the workload or flow after that concept instead of inventing a file-shaped name.

**Architecture doc conflicts**: if a candidate contradicts repo architecture docs or conventions, only surface it when the performance friction is real enough to warrant revisiting the documented shape. Mark it clearly and explain what changed.

Do NOT propose implementation details yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — representative workload, invariants, cost model, optimization mechanism, lifecycle, trade-offs, and verification.

Doc updates happen only when the user has asked for implementation or explicitly authorizes doc edits:

- **Sharpening a fuzzy domain term during the conversation?** Update `UBIQUITOUS_LANGUAGE.md` or its flagged ambiguities only with user agreement.
- **Changing repo structure, module ownership, or architecture behavior?** Update `{repo}/docs/codebase_domains.md`, `{repo}/docs/codebase_architecture.md`, and `{repo}/CONVENTIONS.md` when the change affects those docs.
- **Establishing a durable performance contract or budget?** Record it only when the user accepts the contract and the repository has an appropriate durable location.
- **User rejects the candidate with a load-bearing reason?** Offer to record it in the relevant architecture/conventions docs only when future performance reviews would otherwise re-suggest the same thing. Skip ephemeral reasons and self-evident ones.
- **Want to explore alternative optimizations for the chosen cost center?** See [OPTIMIZATION-DESIGN.md](OPTIMIZATION-DESIGN.md).
