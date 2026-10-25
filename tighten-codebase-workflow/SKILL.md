---
name: tighten-codebase-workflow
description: "Orchestrate codebase typing improvements end to end: run one forked improve-codebase-typing discovery subagent per codebase domain to build an ordered opportunity manifest, assign one planning subagent per candidate, then implement accepted plans in parallel worktrees through a fresh implementer, type-truth verification, focused checks, independent review, finding resolution, closure review, and a scoped typing(domain) commit, then one full repository gate after every plan is integrated. Use only when explicitly invoked as $tighten-codebase-workflow or by name. Do not invoke automatically for related codebase work."
---

# Tighten Codebase Workflow

Run the workflow as the main agent. Retain typing decisions, sequencing, review adjudication, verification acceptance, gate acceptance, staging, and commits. Delegate bounded exploration, implementation, and review tasks.

Invocation authorizes the subagents required by this workflow. Respect repository instructions and user scope throughout.

## Required skills and references

1. Use `improve-codebase-typing` for discovery, vocabulary, type walkthroughs, defect classification, typing discipline, and typing design.
2. Use `doc-creator` for the opportunity manifest and solution plans when available. Repository planning conventions override its default `docs/` placement.
3. Before spawning any workflow subagent, read [references/agent-prompts.md](references/agent-prompts.md) completely and use its contracts.
4. If `improve-codebase-typing` is unavailable, stop and report the missing dependency.

## Invariants

- Give the main agent full initiative within the user's authorized repository and workflow.
- Preserve user and pre-existing changes. Never include unrelated work in a typing commit.
- Preserve valid-input behaviour, domain meaning, and documented ownership unless the accepted plan explicitly changes them.
- Create exactly one solution plan per accepted opportunity.
- Delete workflow-created planning docs when they are no longer needed. Never stage or commit them.
- Run discovery through one forked subagent per domain in `docs/codebase_domains.md`, excluding the documentation domain. Run them concurrently in waves permitted by the agent limit. Give each its own manifest section. The main agent orchestrates discovery only.
- Allow planning agents to run concurrently in waves permitted by the agent limit. Give each a distinct output file.
- Run implementation plans in parallel, each in its own Git worktree created from its baseline. Advance each plan independently as its agents return. Integrate commits onto the workflow branch one at a time.
- Remove each plan's worktree and branch once its commit is integrated.
- Use a fresh implementer agent and a fresh reviewer agent for every plan. Spawn both as non-forked subagents on the main agent's model: the implementer with the highest available effort, the reviewer with effort `high`.
- Reuse the original implementer agent for review resolution.
- Do not let planning, implementation, or reviewer agents commit, push, or modify Git history.
- Require type-truth verification and focused checks after implementation and again after review-driven changes.
- Run the repository's full gate once, after every plan is integrated onto the workflow branch. Before then, run only focused checks: type checking, linting, and focused tests.
- Do not accept added annotations, casts, or suppressions without verified agreement between declared types and runtime values.
- Do not commit with failed type-truth verification, failed focused checks, or unresolved findings.
- Commit only the plan's changes using `typing(<domain>): <succinct message>`.
- Let planning files exceed source-file line guidance when extra detail prevents implementation rediscovery. Remove repetition; retain executable decisions.

## Phase 0: Establish control

1. Read repository instructions, starting docs, architecture/domain language, conventions, notes, and relevant runbooks.
2. Inspect `git status`, current branch, HEAD, and recent commits.
3. Record pre-existing modified, deleted, and untracked paths. Treat them as user-owned unless the workflow creates them.
4. Determine the repository's full gate from its instructions. Prefer the declared aggregate command. If none exists, compose formatting, linting, type checking, tests, and builds appropriate to the repository. Determine the focused checks: type checking, linting, and the tests covering changed code.
5. Determine planning placement from repository instructions. Prefer `planning/project/` when it owns durable plans. Create no parallel planning taxonomy.
6. Record the current branch as the workflow branch. Plan commits integrate onto it.

## Phase 1: Discover opportunities

The main agent orchestrates discovery only. It does not search the codebase, assess candidates, or edit the manifest after creating it.

1. Read `docs/codebase_domains.md`. If it is absent, stop and report the missing domain map.
2. Create the opportunity manifest at the planning placement with one empty section per domain. Exclude the documentation domain.
3. Spawn one forked discovery subagent per section using the discovery prompt contract. Run them concurrently in waves permitted by the agent limit.
4. Each subagent applies `improve-codebase-typing` to its entire domain and leaves no area unexplored. It records, under its own section only, the areas examined with code or type-walkthrough evidence, every credible candidate with an accept, reject, or defer decision and reason, the candidate fields defined in the contract, and a stable domain slug.
5. Before recording a candidate, each subagent checks the other sections and references an existing entry instead of recording a duplicate.
6. Discovery is complete when every subagent has returned and recorded its section.
7. Accepted candidates run in manifest order: domain order, then the order each subagent recorded them.
8. Use `planned`, `implementing`, `reviewing`, `resolving`, and `complete` as workflow statuses for accepted candidates.
9. If the user requested proposal review before execution, pause after the manifest. Otherwise continue through all accepted candidates.

## Phase 2: Produce N solution plans

Begin solution planning only after the Phase 1 discovery completion gate is satisfied.

For `N` accepted candidates:

1. Assign exactly one planning subagent to each candidate using the planning prompt contract. Spawn each as a non-forked subagent on the main agent's model with effort `xhigh`.
2. Give each agent the manifest entry, relevant repository paths, repository instructions, required typing vocabulary, and a unique plan path.
3. Require planning only. Agents may edit only their assigned plan file.
4. Require each plan to contain:
   - value flow and current type walkthrough;
   - evidence and defect category;
   - constraints, preserved valid-input behaviour, and ownership;
   - entry, boundary parse, and declared types;
   - recommended typing change and affected implementation;
   - invalid-input behaviour, nullability, ordering, and error modes;
   - exact migration sequence;
   - escapes, casts, and suppressions to remove;
   - tests to add, replace, and delete;
   - type-truth verification and correctness gate;
   - risks, alternatives, remaining escapes, and acceptance criteria.
5. Review every plan personally. Reconcile overlaps, sequencing dependencies, naming, competing type definitions, shared value flows, and incompatible ownership before implementation.
6. Update the manifest with accepted plan paths and final order.

## Phase 3: Execute plans in parallel

Start plans in manifest order. For each plan, complete 3A and spawn its implementer in 3B, then start the next plan's 3A without waiting. When an agent returns, continue that plan's cycle from where it stopped. Plans advance independently; commits integrate one at a time in 3F.

### 3A. Baseline

1. Record the current HEAD as the plan baseline.
2. Create the plan's worktree and branch from the baseline. Run all implementation, verification, focused-check, and commit work for this plan in that worktree.
3. Identify the files owned by this plan and note overlap with other in-flight plans.
4. Record the baseline type walkthrough and its escapes using the plan's verification surface.
5. Mark the plan `implementing` in the manifest.

### 3B. Implement

1. Spawn a fresh non-forked implementer agent `X` on the main agent's model with the highest available effort, using the implementer prompt contract. Give it the plan's worktree path.
2. Require `X` to implement the accepted plan end to end, remove escapes the plan replaces, update affected durable docs, add regression coverage, run the type-truth verification, and run focused checks.
3. Require exact verification and focused-check commands with key output. A reported pass without command evidence is insufficient.
4. Require `X` to stop without committing.
5. When `X` returns, inspect the resulting diff, status, verification evidence, and focused-check evidence personally. Return out-of-scope changes to `X` for correction without discarding user work.

### 3C. Review

1. Mark the plan `reviewing`.
2. Spawn a fresh non-forked reviewer agent `Y` on the main agent's model with effort `high`, using the reviewer prompt contract.
3. Give `Y` the plan's worktree path, the accepted plan, baseline HEAD, baseline type walkthrough, current plan-owned diff, repository instructions, type-truth verification, and focused-check evidence.
4. Require a read-only, findings-first review. `Y` must not edit files.
5. Scope `Y` to the plan-owned diff. `Y` reads surrounding code only to judge the change and reports only defects in changed code or defects the change introduces. Pre-existing issues outside the diff are out of scope.
6. Require every finding to include severity, exact location, failure mode, and required outcome.

Severity meanings:

- `critical`: security compromise, data loss/corruption, destructive migration, or unusable deployment.
- `high`: functional defect, likely regression, broken contract, ownership violation, false type claim, unparsed boundary, or plan acceptance failure.
- `medium`: precision, documentation, observability, or test weakness with plausible impact.
- `low`: localized clarity, consistency, or minor robustness issue.

### 3D. Resolve findings with X

1. Mark the plan `resolving`.
2. Send the complete review back to the original implementer `X` with the resolution prompt contract.
3. Require a disposition for every finding.
4. Every finding must be fixed or rebutted. `X` may rebut a finding only with concrete code evidence proving it is a false positive. Deferral is not a disposition.
5. Require `X` to update code/tests/docs as appropriate and rerun the type-truth verification and focused checks after its final change.
6. The main agent adjudicates disputes. Never accept a bare disagreement.

### 3E. Close review

1. If the review contained findings, send the final diff and dispositions back to reviewer `Y` using the closure prompt.
2. Repeat resolution and closure while any finding remains valid or a new finding appears.
3. Inspect final status and diff personally.
4. Confirm final type-truth verification and focused-check evidence reflect the post-review tree. Run either as main agent when evidence is incomplete or the tree changed afterward.

### 3F. Commit

1. Derive a concise stable domain slug from the manifest, such as `ingestion-control`, `backfill`, `market-data`, `data-sources`, `api-client`, or `chart-persistence`.
2. Mark the plan `complete` in the manifest, then delete its workflow-created solution plan.
3. In the plan's worktree, stage only implementation files and affected durable docs. Do not stage planning docs.
4. Review the staged diff.
5. Commit with `typing(<domain>): <succinct message>`.
6. Rebase the plan's commit onto the current workflow branch. Resolve conflicts while preserving newer changes. If the rebase changed the base, rerun type-truth verification and focused checks in the worktree.
7. Fast-forward the workflow branch to the rebased commit. Integrate one plan at a time.
8. Verify the commit and clean separation from pre-existing user changes.
9. Record the commit SHA in the main-agent acceptance record. Do not create a manifest-only change solely to record the SHA.
10. Remove the plan's worktree and delete its branch.

## Phase 4: Final gate

After every plan is integrated onto the workflow branch and its worktree removed, run the repository's full gate on the workflow branch as main agent. Record the exact command and key output.

If the full gate fails, spawn one subagent to fix it. That subagent keeps working until the full gate passes.

## Failure and revision handling

- If the plan is materially wrong, pause the current implementation, revise the plan as main agent, and restart the current plan cycle with a fresh implementer. Do not silently diverge.
- If type-truth verification relies on a remaining escape or only restates what the type checker already proves, revise the verification design before accepting the plan.
- If implementation requires changing domain ownership, introducing a seam, or changing valid-input behaviour beyond the accepted scope, report the required scope change before proceeding.
- If focused checks or the final full gate expose a pre-existing failure, prove it against the recorded baseline. The workflow still requires a green final full gate unless the user explicitly changes acceptance.
- If user changes overlap the plan, preserve them and ask only when intent cannot be recovered safely.
- If an agent becomes unavailable, spawn a replacement with the plan, baseline, current diff, and recorded findings. Preserve the plan's cycle and worktree.
- If a destructive action or external authority is required, stop for approval.

## Completion

Finish only when every accepted plan has its own committed implementation and:

- every non-documentation domain has a recorded discovery section with candidate dispositions;
- every targeted value flow's declared types match its runtime values, verified by the type checker and boundary parse tests;
- valid-input behaviour, domain meaning, and accepted ownership remain intact;
- every review finding is fixed or rebutted and closed;
- every plan's final tree passed its focused checks before commit;
- the workflow branch passed the full gate after every plan was integrated;
- commits are scoped and integrated onto the workflow branch;
- no workflow-created worktrees or branches remain;
- durable architecture/convention docs reflect implemented type contracts where affected;
- workflow-created planning docs are deleted and absent from commits;
- pre-existing user changes remain intact.

After all completion conditions are satisfied:

1. Push the completed branch.
2. Report the ordered commits, type-truth verification, gate commands/results, and review dispositions.
