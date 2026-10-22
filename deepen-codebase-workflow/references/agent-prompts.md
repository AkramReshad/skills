---
read_when: Read before spawning discovery, planning, implementation, review, resolution, or closure agents for the deepen-codebase workflow.
last_updated: 2026-10-22
---

# Agent Prompt Contracts

Replace bracketed fields with task-specific facts. Give agents repository paths and raw artifacts. Avoid supplying expected conclusions.

## Discovery agent

```text
Discover architecture deepening opportunities in domain [INDEX]: [DOMAIN].

Repository: [ROOT]
Domain row: [ROW]
Manifest: [MANIFEST_PATH]
Manifest section: [SECTION]

Read repository instructions, docs/codebase_domains.md, relevant architecture docs, and the complete improve-codebase-architecture skill and references. Establish the domain's major responsibilities, module boundaries, and dependency relationships across its scope and key files, and trace them through callers, dependencies, and tests. Apply the deletion test. Examine the entire domain and leave no area unexplored.

Record under [SECTION] only:
- areas examined, with concrete code, dependency, or deletion-test evidence;
- every credible candidate, with an accept, reject, or defer decision and reason;
- problem, proposed deepening, locality/leverage, and test impact;
- files and domains involved;
- stable domain slug;
- status `planned` for accepted candidates, in execution order.

Before recording a candidate, read the other manifest sections. If another section already records the same opportunity, reference that entry instead of recording a duplicate.

Discovery only. Edit only [SECTION] of [MANIFEST_PATH]. Do not change other sections, production code, Git state, or commits. Run the Markdown residue scan and git diff --check for the manifest. Return the section, accepted candidates, and counts of rejected and deferred candidates.
```

## Planning agent

```text
Explore architecture deepening candidate [INDEX]: [TITLE].

Repository: [ROOT]
Manifest entry: [ENTRY]
Output file: [PLAN_PATH]

Read repository instructions, the manifest, relevant architecture/domain docs, and the complete improve-codebase-architecture vocabulary and interface-design references. Trace the current implementation and tests. Apply the deletion test.

Write a standalone solution plan containing:
- evidence and current friction;
- constraints and dependency classifications;
- recommended module placement and ownership;
- explicit interface sketches with invariants, ordering, configuration, and error modes;
- adapters and implementation hidden behind the seam;
- exact phased file migration;
- tests to add, replace, and delete, with the interface as test surface;
- alternatives, risks, decisions, and acceptance criteria.

Planning only. Edit only [PLAN_PATH]. Do not change production code, other plans, Git state, or commits. Planning detail may exceed source-file line guidance when it prevents rediscovery; remove repetition. Run the Markdown residue scan and git diff --check for the file. Return the path, core recommendation, and verification.
```

## Implementer X

```text
Implement accepted architecture deepening plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Manifest: [MANIFEST_PATH]
Baseline HEAD: [SHA]
Pre-existing user paths: [PATHS]
Plan-owned scope: [SCOPE]
Required focused checks: [COMMAND]

Read repository instructions and every document required by the plan. Work only in [WORKTREE_PATH]. Inspect current status/diff before editing. Implement the plan end to end using the simplest repo-native design. Preserve unrelated and pre-existing changes. Update affected durable docs and regression coverage. If repository reality invalidates a material plan decision, stop and report the evidence before diverging.

Run targeted checks while working, then run [COMMAND] against the final tree. Fix failures within scope. Report exact commands and key output. Do not run the full gate. Do not stage, commit, push, rewrite history, or perform destructive Git operations. Return changed files, acceptance evidence, focused-check result, and any blocker.
```

## Reviewer Y

```text
Review the implementation of architecture deepening plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Baseline HEAD: [SHA]
Plan-owned diff/files: [DIFF_OR_PATHS]
Repository instructions: [INSTRUCTION_PATHS]
Reported focused-check evidence: [EVIDENCE]

Review read-only. Do not edit, stage, commit, or push. Review only the plan-owned diff. Read surrounding code only to judge the change. Report only defects in changed code or defects the change introduces; pre-existing issues outside the diff are out of scope. Verify the implementation against the accepted plan, repository contracts, callers, tests, migrations, runtime behavior, and failure modes. Inspect the actual diff and relevant surrounding code. Run read-only or non-mutating checks when useful.

Report findings first, ordered critical, high, medium, low. For each finding include:
- severity;
- exact file and tight line range;
- concrete failure mode or violated contract;
- required outcome;
- evidence sufficient for the implementer to reproduce or rebut it.

Use critical for security/data-loss/destructive-deploy failures; high for correctness/regression/contract/race/acceptance failures; medium for plausible maintainability/performance/observability/test impact; low for localized quality issues. Avoid speculative findings and formatting issues already enforced mechanically. If no findings exist, say so explicitly and list any residual verification risk.
```

## Resolution feedback to X

```text
Resolve the independent review for plan [INDEX]: [TITLE].

Review findings:
[FINDINGS]

Address every finding with a recorded disposition: fix it, or rebut it with concrete code/test evidence proving it is not a real issue. Deferral is not a disposition.

Bare disagreement is insufficient. Preserve the accepted plan and unrelated user changes. Add or adjust regression coverage for valid behavioral findings. After the final edit, rerun targeted checks and the focused checks [COMMAND]. Do not run the full gate, commit, or push.

Return, for each finding: disposition, rationale, files changed, and verification. Include exact final focused-check evidence.
```

## Closure review with Y

```text
Verify closure of the review findings for plan [INDEX]: [TITLE].

Original findings:
[FINDINGS]

Implementer dispositions:
[DISPOSITIONS]

Final diff: [DIFF_OR_PATHS]
Final focused-check evidence: [EVIDENCE]

Review read-only. Confirm whether each finding is fixed or convincingly rebutted. Check for regressions introduced by the resolution. Report only remaining or new findings, with severity and evidence. State explicitly when all findings are closed. Do not edit, stage, commit, or push.
```

## Main-agent acceptance record

For each plan, retain these facts until commitment:

```text
Plan: [INDEX] [TITLE]
Baseline: [SHA]
Worktree: [WORKTREE_PATH]
Implementer: [AGENT]
Reviewer: [AGENT]
Files: [PATHS]
Initial focused checks: [COMMAND + RESULT]
Findings: [SEVERITY + SUMMARY]
Dispositions: [FIXED / REBUTTED + RATIONALE]
Closure: [RESULT]
Final focused checks: [COMMAND + RESULT]
Commit: deepening([DOMAIN]): [MESSAGE]
Commit SHA: [SHA]
```
