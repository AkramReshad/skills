---
name: optimize-codebase-workflow
description: "Orchestrate performance optimization end to end: run improve-codebase-performance, write an ordered opportunity manifest, assign one planning subagent per candidate, then implement each accepted plan sequentially through a fresh implementer, full repository gate, mechanism-matched performance verification, independent review, finding resolution, closure review, and a scoped optimization(domain) commit. Use when the user asks to optimize or improve codebase performance with delegated planning and implementation, or asks to execute performance-optimization proposals as a controlled multi-agent workflow."
---

# Optimize Codebase Workflow

Run the workflow as the main agent. Retain performance decisions, sequencing, review adjudication, verification acceptance, gate acceptance, staging, and commits. Delegate bounded exploration, implementation, and review tasks.

Invocation authorizes the subagents required by this workflow. Respect repository instructions and user scope throughout.

## Required skills and references

1. Use `improve-codebase-performance` for discovery, vocabulary, evidence categories, cost models, optimization mechanisms, invariants, and verification design.
2. Use `doc-creator` for the opportunity manifest and solution plans when available. Repository planning conventions override its default `docs/` placement.
3. Before spawning any workflow subagent, read [references/agent-prompts.md](references/agent-prompts.md) completely and use its contracts.
4. If `improve-codebase-performance` is unavailable, stop and report the missing dependency.

## Invariants

- Give the main agent full initiative within the user's authorized repository and workflow.
- Preserve user and pre-existing changes. Never include unrelated work in an optimization commit.
- Create exactly one solution plan per accepted opportunity.
- Delete workflow-created planning docs when they are no longer needed. Never stage or commit them.
- Allow planning agents to run concurrently in waves permitted by the agent limit. Give each a distinct output file.
- Run implementation plans strictly sequentially. Finish implementation, performance verification, review, resolution, final gate, and commit for plan `i` before starting plan `i + 1`.
- Use a fresh implementer agent and a fresh reviewer agent for every plan.
- Reuse the original implementer agent for review resolution.
- Do not let planning, implementation, or reviewer agents commit, push, or modify Git history.
- Require mechanism-matched performance verification and the repository's full gate after implementation and again after review-driven changes.
- Do not require wall-time measurements when structural proof or a more direct verification surface establishes the cost reduction.
- Do not commit with failed performance verification, a failed full gate, or unresolved critical/high findings.
- Commit only the current plan's changes using `optimization(<domain>): <succinct message>`.
- Let planning files exceed source-file line guidance when extra detail prevents implementation rediscovery. Remove repetition; retain executable decisions.

## Phase 0: Establish control

1. Read repository instructions, starting docs, architecture/domain language, conventions, notes, and relevant runbooks.
2. Inspect `git status`, current branch, HEAD, and recent commits.
3. Record pre-existing modified, deleted, and untracked paths. Treat them as user-owned unless the workflow creates them.
4. Determine the repository's full gate from its instructions. Prefer the declared aggregate command. If none exists, compose formatting, linting, type checking, tests, and builds appropriate to the repository.
5. Determine planning placement from repository instructions. Prefer `planning/project/` when it owns durable plans. Create no parallel planning taxonomy.

## Phase 1: Discover opportunities

1. Apply `improve-codebase-performance` personally as the main agent.
2. Explore the codebase and apply its amplification, scaling, redundant-work, lifecycle, round-trip, work-conservation, critical-path, reuse, and resource-shape tests. Do not delegate the root performance judgment.
3. Write one opportunity manifest containing:
   - ordered candidates;
   - files and domains involved;
   - representative workload, cost center, evidence category, cost model, proposed optimization, and invariants;
   - mechanism-matched verification surface and test impact;
   - stable domain slug for each candidate;
   - solution-plan path and workflow status.
4. Use `planned`, `implementing`, `reviewing`, `resolving`, and `complete` as manifest statuses.
5. If the user requested proposal review before execution, pause after the manifest. Otherwise continue through all candidates.

## Phase 2: Produce N solution plans

For `N` accepted candidates:

1. Assign exactly one planning subagent to each candidate using the planning prompt contract.
2. Give each agent the manifest entry, relevant repository paths, repository instructions, required performance vocabulary, and a unique plan path.
3. Require planning only. Agents may edit only their assigned plan file.
4. Require each plan to contain:
   - representative workload, evidence category, and current cost center;
   - cost model, amplification or scaling mechanism, and constraints;
   - preserved invariants, ordering, lifecycle, and error modes;
   - recommended optimization mechanism and affected implementation;
   - exact migration sequence;
   - tests to add, replace, and delete;
   - mechanism-matched performance verification and correctness gate;
   - risks, alternatives, residual cost, and acceptance criteria.
5. Review every plan personally. Reconcile overlaps, sequencing dependencies, naming, incompatible workload assumptions, and shared cost centers before implementation.
6. Update the manifest with accepted plan paths and final order.

## Phase 3: Execute plan i

Repeat this entire phase for each plan in manifest order. Keep exactly one plan in flight.

### 3A. Baseline

1. Record the current HEAD as the plan baseline.
2. Re-read status and identify the files owned by this plan.
3. Confirm no unresolved overlap with user changes or the preceding optimization.
4. Record the plan's baseline evidence using its verification surface. Use structural proof or cost-model evidence when a repeatable numeric baseline is unavailable or disproportionate.
5. Mark the plan `implementing` in the manifest.

### 3B. Implement

1. Spawn a fresh implementer agent `X` using the implementer prompt contract.
2. Require `X` to implement the accepted plan end to end, update affected durable docs, add regression coverage, run the mechanism-matched performance verification, and run the full gate.
3. Require exact verification and gate commands with key output. A reported pass without command evidence is insufficient.
4. Require `X` to stop without committing.
5. Inspect the resulting diff, status, verification evidence, and gate evidence personally. Return out-of-scope changes to `X` for correction without discarding user work.

### 3C. Review

1. Mark the plan `reviewing`.
2. Spawn a fresh reviewer agent `Y` using the reviewer prompt contract.
3. Give `Y` the accepted plan, baseline HEAD, baseline performance evidence, current plan-owned diff, repository instructions, performance verification evidence, and gate evidence.
4. Require a read-only, findings-first review. `Y` must not edit files.
5. Require every finding to include severity, exact location, failure mode, and required outcome.

Severity meanings:

- `critical`: security compromise, data loss/corruption, destructive migration, or unusable deployment.
- `high`: functional defect, likely regression, broken invariant, race, false performance claim, material cost regression, or plan acceptance failure.
- `medium`: maintainability, observability, verification, residual-cost, or test weakness with plausible impact.
- `low`: localized clarity, consistency, or minor robustness issue.

### 3D. Resolve findings with X

1. Mark the plan `resolving`.
2. Send the complete review back to the original implementer `X` with the resolution prompt contract.
3. Require a disposition for every finding.
4. Critical/high findings must be addressed. `X` may fix them or rebut them with concrete code evidence proving they are false positives.
5. Medium/low findings may be fixed, deferred with a load-bearing rationale, or rebutted as false positives.
6. Require `X` to update code/tests/docs as appropriate and rerun the performance verification and full gate after its final change.
7. The main agent adjudicates disputes. Never accept a bare disagreement.

### 3E. Close review

1. If the review contained critical/high findings, send the final diff and dispositions back to reviewer `Y` using the closure prompt.
2. Repeat resolution and closure while any critical/high finding remains valid or a new critical/high finding appears.
3. Record medium/low dispositions. They do not block commitment when the rationale is technically sound.
4. Inspect final status and diff personally.
5. Confirm final performance-verification and full-gate evidence reflect the post-review tree. Run either as main agent when evidence is incomplete or the tree changed afterward.

### 3F. Commit

1. Derive a concise stable domain slug from the manifest, such as `ingestion-control`, `backfill`, `market-data`, `data-sources`, `test-database`, or `chart-rendering`.
2. Mark the plan `complete` in the manifest, then delete its workflow-created solution plan.
3. Stage only implementation files and affected durable docs. Do not stage planning docs.
4. Review the staged diff.
5. Commit with `optimization(<domain>): <succinct message>`.
6. Verify the commit and clean separation from pre-existing user changes.
7. Record the commit SHA in the main-agent acceptance record. Do not create a manifest-only change solely to record the SHA.
8. Advance to plan `i + 1` only now.

## Failure and revision handling

- If the plan is materially wrong, pause the current implementation, revise the plan as main agent, and restart the current plan cycle with a fresh implementer. Do not silently diverge.
- If performance verification is unstable, mismatched to the mechanism, or incapable of proving the accepted optimization, revise the verification design before accepting the plan. Do not substitute a noisy timing assertion for direct evidence.
- If the full gate exposes a pre-existing failure, prove it against the recorded baseline. The workflow still requires a green final gate unless the user explicitly changes acceptance.
- If user changes overlap the plan, preserve them and ask only when intent cannot be recovered safely.
- If an agent becomes unavailable, spawn a replacement with the plan, baseline, current diff, and recorded findings. Preserve the sequential cycle.
- If a destructive action or external authority is required, stop for approval.

## Completion

Finish only when every accepted plan has its own committed implementation and:

- the targeted cost reduction is verified with evidence matched to its mechanism;
- all stated invariants remain satisfied;
- all critical/high findings are closed;
- all medium/low findings have recorded dispositions;
- every final tree passed its full gate before commit;
- commits are scoped and ordered;
- durable architecture/convention/performance docs reflect implemented behavior where affected;
- workflow-created planning docs are deleted and absent from commits;
- pre-existing user changes remain intact.

After all completion conditions are satisfied:

1. Push the completed branch.
2. Report the ordered commits, performance verification, gate commands/results, review dispositions, and any intentionally deferred medium/low findings.
