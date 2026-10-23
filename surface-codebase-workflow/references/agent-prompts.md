---
read_when: Read before spawning discovery, planning, implementation, review, resolution, or closure agents for the surface-codebase workflow.
last_updated: 2026-10-23
---

# Agent Prompt Contracts

Replace bracketed fields with task-specific facts. Give agents repository paths and raw artifacts. Avoid supplying expected conclusions.

## Discovery agent

```text
Discover codebase error-handling opportunities in domain [INDEX]: [DOMAIN].

Repository: [ROOT]
Domain row: [ROW]
Manifest: [MANIFEST_PATH]
Manifest section: [SECTION]

Read repository instructions, docs/codebase_domains.md, relevant architecture docs, and the complete improve-codebase-error-handling skill and references. Establish the domain's failure paths, from origin through handlers to observer, across its scope and key files, and trace them through callers, dependencies, and tests. Apply the failure-walkthrough, substitution, cause, shape, ownership, catch-scope, fallback, and partial-result tests. Examine the entire domain and leave no area unexplored.

Record under [SECTION] only:
- areas examined, with concrete code or failure-walkthrough evidence;
- every credible candidate, with an accept, reject, or defer decision and reason;
- failure path, current observer outcome, defect category, and evidence;
- proposed handling change, owning layer, and error shape;
- preserved success-path behaviour and ownership;
- failure-injection verification and test impact;
- files and domains involved;
- stable domain slug;
- status `planned` for accepted candidates, in execution order.

Before recording a candidate, read the other manifest sections. If another section already records the same opportunity, reference that entry instead of recording a duplicate.

Discovery only. Edit only [SECTION] of [MANIFEST_PATH]. Do not change other sections, production code, Git state, or commits. Run the Markdown residue scan and git diff --check for the manifest. Return the section, accepted candidates, and counts of rejected and deferred candidates.
```

## Planning agent

```text
Explore codebase error-handling candidate [INDEX]: [TITLE].

Repository: [ROOT]
Manifest entry: [ENTRY]
Output file: [PLAN_PATH]

Read repository instructions, the manifest, relevant architecture/domain docs, and the complete improve-codebase-error-handling vocabulary and error-handling-design references. Trace the failure path, origin, handlers, observer, callers, and tests. Apply the failure-walkthrough, substitution, cause, shape, ownership, catch-scope, fallback, and partial-result tests.

Write a standalone solution plan containing:
- failure path and current failure walkthrough;
- concrete evidence and defect category;
- constraints, preserved success-path behaviour, and ownership;
- owning layer, error shape, and cause preservation;
- recommended handling change and affected implementation;
- fallbacks, partial results, absence states, ordering, and error modes;
- exact phased file and caller migration;
- handlers, catches, fallbacks, and documentation to remove;
- tests to add, replace, and delete;
- failure-injection verification and correctness gate;
- alternatives, risks, residual handling burden, decisions, and acceptance criteria.

Planning only. Edit only [PLAN_PATH]. Do not change production code, other plans, Git state, or commits. Planning detail may exceed source-file line guidance when it prevents rediscovery; remove repetition. Run the Markdown residue scan and git diff --check for the file. Return the path, core recommendation, and verification.
```

## Implementer X

```text
Implement accepted codebase error-handling plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Manifest: [MANIFEST_PATH]
Baseline HEAD: [SHA]
Baseline failure walkthrough: [EVIDENCE]
Pre-existing user paths: [PATHS]
Plan-owned scope: [SCOPE]
Required failure-injection verification: [COMMAND_OR_METHOD]
Required focused checks: [COMMAND]

Read repository instructions and every document required by the plan. Work only in [WORKTREE_PATH]. Inspect current status/diff before editing. Implement the plan end to end using the simplest repo-native design. Preserve unrelated and pre-existing changes, success-path behaviour, domain meaning, and accepted ownership. Remove handlers the plan replaces. Update affected durable docs and regression coverage. If repository reality invalidates a material plan decision, stop and report the evidence before diverging.

Run targeted checks while working, then run [COMMAND_OR_METHOD] and [COMMAND] against the final tree. Fix failures within scope. Report exact commands and key output, including evidence that the injected failure reaches its observer explicitly, in the standard error shape, with its cause. Do not run the full gate. Do not stage, commit, push, rewrite history, or perform destructive Git operations. Return changed files, acceptance evidence, failure-injection verification, focused-check result, and any blocker.
```

## Reviewer Y

```text
Review the implementation of codebase error-handling plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Baseline HEAD: [SHA]
Baseline failure walkthrough: [EVIDENCE]
Plan-owned diff/files: [DIFF_OR_PATHS]
Repository instructions: [INSTRUCTION_PATHS]
Reported failure-injection verification: [EVIDENCE]
Reported focused-check evidence: [EVIDENCE]

Review read-only. Do not edit, stage, commit, or push. Review only the plan-owned diff. Read surrounding code only to judge the change. Report only defects in changed code or defects the change introduces; pre-existing issues outside the diff are out of scope. Verify the implementation against the accepted plan, failure path, defect evidence, owning layer, error shape, cause preservation, preserved success-path behaviour and ownership, repository contracts, callers, tests, migrations, runtime behaviour, and failure modes. Confirm that replaced handlers are removed and that the verification injects the failure at its origin and asserts what the observer receives. Inspect the actual diff and relevant surrounding code. Run read-only or non-mutating checks when useful.

Report findings first, ordered critical, high, medium, low. For each finding include:
- severity;
- exact file and tight line range;
- concrete failure mode or violated contract;
- required outcome;
- evidence sufficient for the implementer to reproduce or rebut it.

Use critical for security/data-loss/destructive-deploy failures; high for correctness/regression/contract/ownership/silent-failure/lost-cause/false-error-handling-claim/acceptance failures; medium for plausible error-shape/documentation/observability/test impact; low for localized quality issues. Avoid speculative findings and formatting issues already enforced mechanically. If no findings exist, say so explicitly and list any residual verification risk.
```

## Resolution feedback to X

```text
Resolve the independent review for plan [INDEX]: [TITLE].

Review findings:
[FINDINGS]

Address every finding with a recorded disposition: fix it, or rebut it with concrete code/test/failure-walkthrough evidence proving it is not a real issue. Deferral is not a disposition.

Bare disagreement is insufficient. Preserve the accepted plan, success-path behaviour, domain meaning, accepted ownership, and unrelated user changes. Add or adjust regression coverage for valid behavioural findings. After the final edit, rerun targeted checks, the failure-injection verification [COMMAND_OR_METHOD], and the focused checks [COMMAND]. Do not run the full gate, commit, or push.

Return, for each finding: disposition, rationale, files changed, and verification. Include exact final failure-injection and focused-check evidence.
```

## Closure review with Y

```text
Verify closure of the review findings for plan [INDEX]: [TITLE].

Original findings:
[FINDINGS]

Implementer dispositions:
[DISPOSITIONS]

Final diff: [DIFF_OR_PATHS]
Final failure-injection verification: [EVIDENCE]
Final focused-check evidence: [EVIDENCE]

Review read-only. Confirm whether each finding is fixed or convincingly rebutted. Check for regressions introduced by the resolution and confirm the targeted failure still reaches its observer explicitly, in the standard error shape, with its cause. Report only remaining or new findings, with severity and evidence. State explicitly when all findings are closed. Do not edit, stage, commit, or push.
```

## Main-agent acceptance record

For each plan, retain these facts until commitment:

```text
Plan: [INDEX] [TITLE]
Baseline: [SHA]
Worktree: [WORKTREE_PATH]
Failure path: [PATH]
Defect and category: [DEFECT + CATEGORY]
Baseline failure walkthrough: [EVIDENCE]
Implementer: [AGENT]
Reviewer: [AGENT]
Files: [PATHS]
Initial failure-injection verification: [COMMAND_OR_METHOD + RESULT]
Initial focused checks: [COMMAND + RESULT]
Findings: [SEVERITY + SUMMARY]
Dispositions: [FIXED / REBUTTED + RATIONALE]
Closure: [RESULT]
Final failure-injection verification: [COMMAND_OR_METHOD + RESULT]
Final focused checks: [COMMAND + RESULT]
Commit: error-handling([DOMAIN]): [MESSAGE]
Commit SHA: [SHA]
```
