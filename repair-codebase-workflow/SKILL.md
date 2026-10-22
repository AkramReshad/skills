---
name: repair-codebase-workflow
description: "Orchestrate codebase repairs end to end: run improve-codebase-quality across every domain, write an ordered issue manifest, assign one planning subagent per nonempty domain/severity group, then implement accepted plans in parallel worktrees through a fresh implementer, focused checks, independent review, finding resolution, closure review, and a scoped repair(domain) commit, then one full repository gate after every plan is integrated. Use only when explicitly invoked as $repair-codebase-workflow or by name. Do not invoke automatically for related codebase work."
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
- Process all validated source issues regardless of severity.
- Keep persistent review artifacts ignored and uncommitted. Do not delete accepted non-issues during planning cleanup.
- Delete workflow-created planning docs when they are no longer needed. Never stage or commit them.
- Allow planning agents to run concurrently in waves permitted by the agent limit. Give each a distinct output file.
- Run implementation plans in parallel, each in its own Git worktree created from its baseline. Advance each plan independently as its agents return. Integrate commits onto the workflow branch one at a time.
- Remove each plan's worktree and branch once its commit is integrated.
- Use a fresh implementer agent and a fresh reviewer agent for every plan. Spawn both as non-forked subagents on the main agent's model: the implementer with the highest available effort, the reviewer with effort `high`.
- Reuse the original implementer agent for review resolution.
- Do not let planning, implementation, or reviewer agents commit, push, or modify Git history.
- Require focused checks after implementation and again after review-driven changes.
- Run the repository's full gate once, after every plan is integrated onto the workflow branch. Before then, run only focused checks: type checking, linting, and focused tests.
- Do not commit with failed focused checks or unresolved findings.
- Commit only the plan's changes using `repair(<domain>): <succinct message>`.
- Let planning files exceed source-file line guidance when extra detail prevents implementation rediscovery. Remove repetition; retain executable decisions.

## Phase 0: Establish control

1. Read repository instructions, starting docs, architecture/domain language, conventions, notes, and relevant runbooks.
2. Inspect `git status`, current branch, HEAD, and recent commits.
3. Record pre-existing modified, deleted, and untracked paths. Treat them as user-owned unless the workflow creates them.
4. Determine the repository's full gate from its instructions. Prefer the declared aggregate command. If none exists, compose formatting, linting, type checking, tests, and builds appropriate to the repository. Determine the focused checks: type checking, linting, and the tests covering changed code.
5. Determine planning placement from repository instructions. Prefer `planning/project/` when it owns durable plans. Create no parallel planning taxonomy.
6. Record the current branch as the workflow branch. Plan commits integrate onto it.

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

1. Partition all validated issues by domain into three severity groups: `critical`, `high`, and `remaining`, which holds the Medium, Low, NIT, and Tests sections. Create no empty groups. Assign exactly one planning subagent to each group using the planning prompt contract. Spawn each as a non-forked subagent on the main agent's model with effort `xhigh`. Do not create separate assignments for individual issues within a group.
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

## Phase 3: Execute plans in parallel

Start domain/severity group plans in manifest order. For each plan, complete 3A and spawn its implementer in 3B, then start the next plan's 3A without waiting. When an agent returns, continue that plan's cycle from where it stopped. Plans advance independently; commits integrate one at a time in 3F. Each plan's implementer and reviewer each handle the entire group; do not spawn separate agents for individual source issues.

### 3A. Baseline

1. Record the current HEAD as the plan baseline.
2. Create the plan's worktree and branch from the baseline. Run all implementation, verification, focused-check, and commit work for this plan in that worktree.
3. Identify the files owned by this plan and note overlap with other in-flight plans.
4. Revalidate every source issue in the group against the current tree. If a preceding repair resolved an issue, verify that outcome, record it as resolved, and remove its local issue entry. Continue with all remaining issues in the same group plan. If every issue is already resolved, delete the workflow-created plan, remove its worktree and branch, and end the plan without creating an empty commit.
5. Mark the plan `implementing` in the manifest.

### 3B. Implement

1. Spawn a fresh non-forked implementer agent `X` on the main agent's model with the highest available effort, using the implementer prompt contract. Give it the plan's worktree path.
2. Require `X` to implement the accepted plan end to end, update affected durable docs, add regression coverage where appropriate, run the issue-specific verification, and run focused checks.
3. Require exact issue-specific verification and focused-check commands and key output. A reported pass without command evidence is insufficient.
4. Require `X` to stop without committing.
5. When `X` returns, inspect the resulting diff, status, and focused-check evidence personally. Return out-of-scope changes to `X` for correction without discarding user work.

### 3C. Review

1. Mark the plan `reviewing`.
2. Spawn a fresh non-forked reviewer agent `Y` on the main agent's model with effort `high`, using the reviewer prompt contract.
3. Give `Y` the plan's worktree path, the accepted plan, baseline HEAD, current plan-owned diff, repository instructions, and focused-check evidence.
4. Require a read-only, findings-first review. `Y` must not edit files.
5. Scope `Y` to the plan-owned diff. `Y` reads surrounding code only to judge the change and reports only defects in changed code or defects the change introduces. Pre-existing issues outside the diff are out of scope.
6. Require every finding to include severity, exact location, failure mode, and required outcome.

Severity meanings:

- `critical`: security compromise, data loss/corruption, destructive migration, or unusable deployment.
- `high`: functional defect, likely regression, broken contract, race, or plan acceptance failure.
- `medium`: maintainability, performance, observability, or test weakness with plausible impact.
- `low`: localized clarity, consistency, or minor robustness issue.

### 3D. Resolve findings with X

1. Mark the plan `resolving`.
2. Send the complete review back to the original implementer `X` with the resolution prompt contract.
3. Require a disposition for every finding.
4. Every finding must be fixed or rebutted. `X` may rebut a finding only with concrete code evidence proving it is a false positive. Deferral is not a disposition.
5. Require `X` to update code/tests/docs as appropriate and rerun the issue-specific verification and focused checks after its final change.
6. The main agent adjudicates disputes. Never accept a bare disagreement.

### 3E. Close review

1. If the review contained findings, send the final diff and dispositions back to reviewer `Y` using the closure prompt.
2. Repeat resolution and closure while any finding remains valid or a new finding appears.
3. Inspect final status and diff personally.
4. Confirm final issue-specific verification and focused-check evidence reflect the post-review tree. Run the focused checks as main agent when evidence is incomplete or the tree changed afterward.

### 3F. Commit

1. Derive a concise stable domain slug from the manifest, such as `ingestion-control`, `backfill`, `market-data`, `data-sources`, or `chart-persistence`.
2. Verify every source issue in the group is resolved, remove its entry from the local domain issue file, mark the group plan `complete` in the manifest, then delete its workflow-created solution plan. Keep unresolved findings and accepted non-issues intact.
3. In the plan's worktree, stage only implementation files and affected durable docs. Do not stage planning docs or `code_review/` artifacts.
4. Review the staged diff.
5. Commit with `repair(<domain>): <succinct message>`.
6. Rebase the plan's commit onto the current workflow branch. Resolve conflicts while preserving newer changes. If the rebase changed the base, rerun the issue-specific verification and focused checks in the worktree.
7. Fast-forward the workflow branch to the rebased commit. Integrate one plan at a time.
8. Verify the commit and clean separation from pre-existing user changes.
9. Record the commit SHA in the main-agent acceptance record. Do not create a manifest-only change solely to record the SHA.
10. Remove the plan's worktree and delete its branch.

## Phase 4: Final gate

After every plan is integrated onto the workflow branch and its worktree removed, run the repository's full gate on the workflow branch as main agent. Record the exact command and key output.

If the full gate fails, spawn one subagent to fix it. That subagent keeps working until the full gate passes.

## Failure and revision handling

- If the plan is materially wrong, pause the current implementation, revise the plan as main agent, and restart the current plan cycle with a fresh implementer. Do not silently diverge.
- If focused checks or the final full gate expose a pre-existing failure, prove it against the recorded baseline. The workflow still requires a green final full gate unless the user explicitly changes acceptance.
- If user changes overlap the plan, preserve them and ask only when intent cannot be recovered safely.
- If an agent becomes unavailable, spawn a replacement with the plan, baseline, current diff, and recorded findings. Preserve the plan's cycle and worktree.
- If a destructive action or external authority is required, stop for approval.

## Completion

Finish only when every validated issue has a committed repair or evidence that an earlier repair resolved it, and:

- every review finding is fixed or rebutted and closed;
- every plan's final tree passed its focused checks before commit;
- the workflow branch passed the full gate after every plan was integrated;
- commits are scoped and integrated onto the workflow branch;
- no workflow-created worktrees or branches remain;
- issue-specific verification proves each repaired issue is resolved;
- durable docs reflect implemented behaviour where affected;
- local issue files reflect remaining findings and accepted non-issues;
- `code_review/` artifacts are absent from commits;
- workflow-created planning docs are deleted and absent from commits;
- pre-existing user changes remain intact.

After all completion conditions are satisfied:

1. Push the completed branch.
