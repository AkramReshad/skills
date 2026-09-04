---
name: streamline-codebase-workflow
description: "Orchestrate codebase ergonomics improvements end to end: run improve-codebase-ergonomics, write an ordered opportunity manifest, assign one planning subagent per candidate, then implement each accepted plan sequentially through a fresh implementer, representative-task verification, full repository gate, independent review, finding resolution, closure review, and a scoped ergonomics(domain) commit. Use when the user asks to streamline or improve codebase ergonomics with delegated planning and implementation, or asks to execute ergonomics proposals as a controlled multi-agent workflow."
---

# Streamline Codebase Workflow

Run the workflow as the main agent. Retain ergonomics decisions, sequencing, review adjudication, verification acceptance, gate acceptance, staging, and commits. Delegate bounded exploration, implementation, and review tasks.

Invocation authorizes the subagents required by this workflow. Respect repository instructions and user scope throughout.

## Required skills and references

1. Use `improve-codebase-ergonomics` for discovery, vocabulary, task walkthroughs, friction classification, canonical-path discipline, and ergonomic design.
2. Use `doc-creator` for the opportunity manifest and solution plans when available. Repository planning conventions override its default `docs/` placement.
3. Before spawning any workflow subagent, read [references/agent-prompts.md](references/agent-prompts.md) completely and use its contracts.
4. If `improve-codebase-ergonomics` is unavailable, stop and report the missing dependency.

## Invariants

- Give the main agent full initiative within the user's authorized repository and workflow.
- Preserve user and pre-existing changes. Never include unrelated work in an ergonomics commit.
- Preserve runtime behaviour, domain meaning, and documented ownership unless the accepted plan explicitly changes them.
- Create exactly one solution plan per accepted opportunity.
- Delete workflow-created planning docs when they are no longer needed. Never stage or commit them.
- Allow planning agents to run concurrently in waves permitted by the agent limit. Give each a distinct output file.
- Run implementation plans strictly sequentially. Finish implementation, representative-task verification, review, resolution, final gate, and commit for plan `i` before starting plan `i + 1`.
- Use a fresh implementer agent and a fresh reviewer agent for every plan.
- Reuse the original implementer agent for review resolution.
- Do not let planning, implementation, or reviewer agents commit, push, or modify Git history.
- Require representative-task verification and the repository's full gate after implementation and again after review-driven changes.
- Do not accept aesthetic preference, file movement, helper addition, or line-count reduction without verified friction reduction and a canonical path.
- Do not commit with failed representative-task verification, a failed full gate, or unresolved critical/high findings.
- Commit only the current plan's changes using `ergonomics(<domain>): <succinct message>`.
- Let planning files exceed source-file line guidance when extra detail prevents implementation rediscovery. Remove repetition; retain executable decisions.

## Phase 0: Establish control

1. Read repository instructions, starting docs, architecture/domain language, conventions, notes, and relevant runbooks.
2. Inspect `git status`, current branch, HEAD, and recent commits.
3. Record pre-existing modified, deleted, and untracked paths. Treat them as user-owned unless the workflow creates them.
4. Determine the repository's full gate from its instructions. Prefer the declared aggregate command. If none exists, compose formatting, linting, type checking, tests, and builds appropriate to the repository.
5. Determine planning placement from repository instructions. Prefer `planning/project/` when it owns durable plans. Create no parallel planning taxonomy.

## Phase 1: Discover opportunities

1. Apply `improve-codebase-ergonomics` personally as the main agent.
2. Explore the codebase and apply its task-walkthrough, canonical-path, organization, discoverability, ceremony, choice, common-path, and residue tests. Do not delegate the root ergonomics judgment.
3. Write one opportunity manifest containing:
   - ordered candidates;
   - files and domains involved;
   - representative task, current surface, friction category, and evidence;
   - proposed organization or convenience improvement and canonical path;
   - preserved behaviour and ownership;
   - representative-task verification and test impact;
   - stable domain slug for each candidate;
   - solution-plan path and workflow status.
4. Use `planned`, `implementing`, `reviewing`, `resolving`, and `complete` as manifest statuses.
5. If the user requested proposal review before execution, pause after the manifest. Otherwise continue through all candidates.

## Phase 2: Produce N solution plans

For `N` accepted candidates:

1. Assign exactly one planning subagent to each candidate using the planning prompt contract.
2. Give each agent the manifest entry, relevant repository paths, repository instructions, required ergonomics vocabulary, and a unique plan path.
3. Require planning only. Agents may edit only their assigned plan file.
4. Require each plan to contain:
   - representative task and current task walkthrough;
   - evidence and friction category;
   - constraints, preserved behaviour, and ownership;
   - recommended organization or usage surface and canonical path;
   - required choices, defaults, ordering, and error modes;
   - exact migration sequence;
   - obsolete paths, aliases, helpers, exports, and documentation to delete;
   - tests to add, replace, and delete;
   - representative-task verification and correctness gate;
   - risks, alternatives, residual friction, and acceptance criteria.
5. Review every plan personally. Reconcile overlaps, sequencing dependencies, naming, competing canonical paths, and incompatible ownership before implementation.
6. Update the manifest with accepted plan paths and final order.

## Phase 3: Execute plan i

Repeat this entire phase for each plan in manifest order. Keep exactly one plan in flight.

### 3A. Baseline

1. Record the current HEAD as the plan baseline.
2. Re-read status and identify the files owned by this plan.
3. Confirm no unresolved overlap with user changes or the preceding ergonomics improvement.
4. Record the baseline task walkthrough and its friction evidence using the plan's verification surface.
5. Mark the plan `implementing` in the manifest.

### 3B. Implement

1. Spawn a fresh implementer agent `X` using the implementer prompt contract.
2. Require `X` to implement the accepted plan end to end, migrate representative callers, delete obsolete paths and residue, update affected durable docs, add regression coverage, run the representative-task verification, and run the full gate.
3. Require exact verification and gate commands with key output. A reported pass without command evidence is insufficient.
4. Require `X` to stop without committing.
5. Inspect the resulting diff, status, verification evidence, and gate evidence personally. Return out-of-scope changes to `X` for correction without discarding user work.

### 3C. Review

1. Mark the plan `reviewing`.
2. Spawn a fresh reviewer agent `Y` using the reviewer prompt contract.
3. Give `Y` the accepted plan, baseline HEAD, baseline task walkthrough, current plan-owned diff, repository instructions, representative-task verification, and gate evidence.
4. Require a read-only, findings-first review. `Y` must not edit files.
5. Require every finding to include severity, exact location, failure mode, and required outcome.

Severity meanings:

- `critical`: security compromise, data loss/corruption, destructive migration, or unusable deployment.
- `high`: functional defect, likely regression, broken contract, ownership violation, competing canonical path, false ergonomics claim, material residue, or plan acceptance failure.
- `medium`: discoverability, ceremony, cognitive-load, documentation, observability, or test weakness with plausible impact.
- `low`: localized clarity, consistency, or minor robustness issue.

### 3D. Resolve findings with X

1. Mark the plan `resolving`.
2. Send the complete review back to the original implementer `X` with the resolution prompt contract.
3. Require a disposition for every finding.
4. Critical/high findings must be addressed. `X` may fix them or rebut them with concrete code evidence proving they are false positives.
5. Medium/low findings may be fixed, deferred with a load-bearing rationale, or rebutted as false positives.
6. Require `X` to update code/tests/docs as appropriate and rerun the representative-task verification and full gate after its final change.
7. The main agent adjudicates disputes. Never accept a bare disagreement.

### 3E. Close review

1. If the review contained critical/high findings, send the final diff and dispositions back to reviewer `Y` using the closure prompt.
2. Repeat resolution and closure while any critical/high finding remains valid or a new critical/high finding appears.
3. Record medium/low dispositions. They do not block commitment when the rationale is technically sound.
4. Inspect final status and diff personally.
5. Confirm final representative-task verification and full-gate evidence reflect the post-review tree. Run either as main agent when evidence is incomplete or the tree changed afterward.

### 3F. Commit

1. Derive a concise stable domain slug from the manifest, such as `backend-tests`, `market-data`, `test-fixtures`, `api-client`, `commands`, or `configuration`.
2. Mark the plan `complete` in the manifest, then delete its workflow-created solution plan.
3. Stage only implementation files and affected durable docs. Do not stage planning docs.
4. Review the staged diff.
5. Commit with `ergonomics(<domain>): <succinct message>`.
6. Verify the commit and clean separation from pre-existing user changes.
7. Record the commit SHA in the main-agent acceptance record. Do not create a manifest-only change solely to record the SHA.
8. Advance to plan `i + 1` only now.

## Failure and revision handling

- If the plan is materially wrong, pause the current implementation, revise the plan as main agent, and restart the current plan cycle with a fresh implementer. Do not silently diverge.
- If representative-task verification does not establish reduced friction or relies on a brittle syntax/line-count assertion, revise the verification design before accepting the plan.
- If implementation requires changing ownership, introducing a seam, concentrating distributed invariants, or optimizing runtime cost beyond the accepted plan, stop and report that the candidate crosses into architecture or performance work.
- If the full gate exposes a pre-existing failure, prove it against the recorded baseline. The workflow still requires a green final gate unless the user explicitly changes acceptance.
- If user changes overlap the plan, preserve them and ask only when intent cannot be recovered safely.
- If an agent becomes unavailable, spawn a replacement with the plan, baseline, current diff, and recorded findings. Preserve the sequential cycle.
- If a destructive action or external authority is required, stop for approval.

## Completion

Finish only when every accepted plan has its own committed implementation and:

- the representative task has a verified reduction in friction;
- one canonical path remains and obsolete residue is removed;
- runtime behaviour, domain meaning, and accepted ownership remain intact;
- all critical/high findings are closed;
- all medium/low findings have recorded dispositions;
- every final tree passed its full gate before commit;
- commits are scoped and ordered;
- durable architecture/convention docs reflect implemented organization and canonical usage where affected;
- workflow-created planning docs are deleted and absent from commits;
- pre-existing user changes remain intact.

After all completion conditions are satisfied:

1. Push the completed branch.
2. Report the ordered commits, representative-task verification, gate commands/results, review dispositions, and any intentionally deferred medium/low findings.
