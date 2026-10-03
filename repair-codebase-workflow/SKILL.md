---
name: repair-codebase-workflow
description: "Orchestrate codebase repairs end to end: run improve-codebase-quality across every domain, write an ordered issue manifest, assign one planning subagent per nonempty domain/severity group, then implement each accepted plan sequentially through a fresh implementer, full repository gate, independent review, finding resolution, closure review, and a scoped repair(domain) commit. Use when the user asks to find and fix codebase quality issues with delegated planning and implementation, or asks to execute comprehensive domain review findings as a controlled multi-agent workflow."
---

# Repair Codebase Workflow

Run the workflow as the main agent. Retain quality decisions, sequencing, review adjudication, gate acceptance, staging, and commits. Delegate bounded exploration, implementation, and review tasks.

Invocation authorizes the subagents required by this workflow. Respect repository instructions and user scope throughout.

## Required skills and references

1. Use `improve-codebase-quality` for complete domain review, vocabulary, issue validation, accepted non-issues, and fix guidance.
2. Use `doc-creator` for the issue manifest and solution plans when available. Repository planning conventions override its default `docs/` placement.
3. Before spawning any workflow subagent, read [references/agent-prompts.md](references/agent-prompts.md) completely and use its contracts.
4. If `improve-codebase-quality` is unavailable, stop and report the missing dependency.

## Invariants

- Give the main agent full initiative within the user's authorized repository and workflow.
- Preserve user and pre-existing changes. Never include unrelated work in a repair commit.
- Assign agents per nonempty domain/severity group, such as `ingestion/critical` or `ingestion/high`. Each assignment covers every source issue in that group. Never spawn an agent per source issue.
- Create exactly one solution plan per nonempty domain/severity group.
- Process all validated source issues regardless of severity. Medium/low deferral below applies only to findings raised during implementation review.
- Keep persistent review artifacts ignored and uncommitted. Do not delete accepted non-issues during planning cleanup.
- Delete workflow-created planning docs when they are no longer needed. Never stage or commit them.
- Allow planning agents to run concurrently in waves permitted by the agent limit. Give each a distinct output file.
- Run implementation plans strictly sequentially. Finish implementation, review, resolution, final gate, and commit for plan `i` before starting plan `i + 1`.
- Use a fresh implementer agent and a fresh reviewer agent for every plan.
- Reuse the original implementer agent for review resolution.
- Do not let planning, implementation, or reviewer agents commit, push, or modify Git history.
- Require the repository's full gate after implementation and again after review-driven changes.
- Do not commit with a failed full gate or unresolved critical/high findings.
- Commit only the current plan's changes using `repair(<domain>): <succinct message>`.
- Let planning files exceed source-file line guidance when extra detail prevents implementation rediscovery. Remove repetition; retain executable decisions.

## Phase 0: Establish control

1. Read repository instructions, starting docs, architecture/domain language, conventions, notes, and relevant runbooks.
2. Inspect `git status`, current branch, HEAD, and recent commits.
3. Record pre-existing modified, deleted, and untracked paths. Treat them as user-owned unless the workflow creates them.
4. Determine the repository's full gate from its instructions. Prefer the declared aggregate command. If none exists, compose formatting, linting, type checking, tests, and builds appropriate to the repository.
5. Determine planning placement from repository instructions. Prefer `planning/project/` when it owns durable plans. Create no parallel planning taxonomy.

## Phase 1: Discover and validate all issues

1. Apply `improve-codebase-quality` as the main agent, coordinating its domain reviewers and separate validation agents. Complete both passes for every domain before planning implementations.
2. Retain every validated issue, including existing valid issues. Do not limit findings or select one or two candidates. Reconcile duplicates and accepted non-issues personally.
3. Write one issue manifest containing:
   - all validated issues, ordered by severity and implementation dependencies;
   - stable issue IDs, source issue-file paths, files and domains involved;
   - category, severity, evidence, concrete trigger, and consequence;
   - validated Industry Standard Fix guidance and verification;
   - stable domain slug for each issue;
   - domain/severity group, shared solution-plan path, and workflow status.
4. Use `planned`, `implementing`, `reviewing`, `resolving`, and `complete` as manifest statuses.
5. If the user requested proposal review before execution, pause after the manifest. Otherwise continue through all validated issues. Respect any explicitly scoped exclusions.
6. Keep `code_review/` ignored and uncommitted, including issue files and `non-issues.md`. The discovery skill's prohibition on implementation and commits applies to discovery; the following phases authorize implementation and scoped commits.

## Phase 2: Produce N solution plans

For `N` nonempty domain/severity groups:

1. Partition all validated issues by domain and their recorded severity or issue-file section, including NIT and Tests when present. Create no empty groups. Assign exactly one planning subagent to each group using the planning prompt contract. Do not create separate assignments for individual issues within a group.
2. Give each agent all manifest entries for its domain/severity group, relevant repository paths, repository instructions, required quality vocabulary, and a unique plan path.
3. Require planning only. Agents may edit only their assigned plan file.
4. Require each plan to contain:
   - domain/severity group and every source issue ID, category, severity, and current-code validation;
   - concrete trigger, evidence, consequence, and root cause for each source issue;
   - constraints and accepted non-issues;
   - recommended fix and affected implementation;
   - preserved invariants, ordering, and error modes;
   - exact migration sequence;
   - tests to add, replace, and delete;
   - issue-specific verification for every source issue and the correctness gate;
   - risks, alternatives, and acceptance criteria.
5. Review every plan personally. Reconcile overlaps, sequencing dependencies, naming, and incompatible ownership before implementation.
6. Update the manifest with accepted plan paths and final order.

## Phase 3: Execute plan i

Repeat this entire phase for each domain/severity group plan in manifest order. Keep exactly one plan in flight. Its implementer and reviewer each handle the entire group; do not spawn separate agents for individual source issues.

### 3A. Baseline

1. Record the current HEAD as the plan baseline.
2. Re-read status and identify the files owned by this plan.
3. Confirm no unresolved overlap with user changes or the preceding repair.
4. Revalidate every source issue in the group against the current tree. If a preceding repair resolved an issue, verify that outcome, record it as resolved, and remove its local issue entry. Continue with all remaining issues in the same group plan. If every issue is already resolved, delete the workflow-created plan and advance without creating an empty commit.
5. Mark the plan `implementing` in the manifest.

### 3B. Implement

1. Spawn a fresh implementer agent `X` using the implementer prompt contract.
2. Require `X` to implement the accepted plan end to end, update affected durable docs, add regression coverage where appropriate, run the issue-specific verification, and run the full gate.
3. Require exact issue-specific verification and gate commands and key output. A reported pass without command evidence is insufficient.
4. Require `X` to stop without committing.
5. Inspect the resulting diff, status, and gate evidence personally. Return out-of-scope changes to `X` for correction without discarding user work.

### 3C. Review

1. Mark the plan `reviewing`.
2. Spawn a fresh reviewer agent `Y` using the reviewer prompt contract.
3. Give `Y` the accepted plan, baseline HEAD, current plan-owned diff, repository instructions, and gate evidence.
4. Require a read-only, findings-first review. `Y` must not edit files.
5. Require every finding to include severity, exact location, failure mode, and required outcome.

Severity meanings:

- `critical`: security compromise, data loss/corruption, destructive migration, or unusable deployment.
- `high`: functional defect, likely regression, broken contract, race, or plan acceptance failure.
- `medium`: maintainability, performance, observability, or test weakness with plausible impact.
- `low`: localized clarity, consistency, or minor robustness issue.

### 3D. Resolve findings with X

1. Mark the plan `resolving`.
2. Send the complete review back to the original implementer `X` with the resolution prompt contract.
3. Require a disposition for every finding.
4. Critical/high findings must be addressed. `X` may fix them or rebut them with concrete code evidence proving they are false positives.
5. Medium/low findings may be fixed, deferred with a load-bearing rationale, or rebutted as false positives.
6. Require `X` to update code/tests/docs as appropriate and rerun the issue-specific verification and full gate after its final change.
7. The main agent adjudicates disputes. Never accept a bare disagreement.

### 3E. Close review

1. If the review contained critical/high findings, send the final diff and dispositions back to reviewer `Y` using the closure prompt.
2. Repeat resolution and closure while any critical/high finding remains valid or a new critical/high finding appears.
3. Record medium/low dispositions. They do not block commitment when the rationale is technically sound.
4. Inspect final status and diff personally.
5. Confirm final issue-specific verification and full-gate evidence reflect the post-review tree. Run the gate as main agent when evidence is incomplete or the tree changed afterward.

### 3F. Commit

1. Derive a concise stable domain slug from the manifest, such as `ingestion-control`, `backfill`, `market-data`, `data-sources`, or `chart-persistence`.
2. Verify every source issue in the group is resolved, remove its entry from the local domain issue file, mark the group plan `complete` in the manifest, then delete its workflow-created solution plan. Keep unresolved findings and accepted non-issues intact.
3. Stage only implementation files and affected durable docs. Do not stage planning docs or `code_review/` artifacts.
4. Review the staged diff.
5. Commit with `repair(<domain>): <succinct message>`.
6. Verify the commit and clean separation from pre-existing user changes.
7. Record the commit SHA in the main-agent acceptance record. Do not create a manifest-only change solely to record the SHA.
8. Advance to plan `i + 1` only now.

## Failure and revision handling

- If the plan is materially wrong, pause the current implementation, revise the plan as main agent, and restart the current plan cycle with a fresh implementer. Do not silently diverge.
- If the full gate exposes a pre-existing failure, prove it against the recorded baseline. The workflow still requires a green final gate unless the user explicitly changes acceptance.
- If user changes overlap the plan, preserve them and ask only when intent cannot be recovered safely.
- If an agent becomes unavailable, spawn a replacement with the plan, baseline, current diff, and recorded findings. Preserve the sequential cycle.
- If a destructive action or external authority is required, stop for approval.

## Completion

Finish only when every validated issue has a committed repair or evidence that an earlier repair resolved it, and:

- all critical/high findings are closed;
- all medium/low findings have recorded dispositions;
- every final tree passed its full gate before commit;
- commits are scoped and ordered;
- issue-specific verification proves each repaired issue is resolved;
- durable docs reflect implemented behaviour where affected;
- local issue files reflect remaining findings and accepted non-issues;
- `code_review/` artifacts are absent from commits;
- workflow-created planning docs are deleted and absent from commits;
- pre-existing user changes remain intact.

After all completion conditions are satisfied:

1. Push the completed branch.

Deferral rules for implementation-review findings do not authorize skipping source issues.
