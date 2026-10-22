---
read_when: Read before spawning discovery, planning, implementation, review, resolution, or closure agents for the clarify-codebase workflow.
last_updated: 2026-10-22
---

# Agent Prompt Contracts

Replace bracketed fields with task-specific facts. Give agents repository paths and raw artifacts. Avoid supplying expected conclusions.

## Discovery agent

```text
Discover codebase readability opportunities in domain [INDEX]: [DOMAIN].

Repository: [ROOT]
Domain row: [ROW]
Manifest: [MANIFEST_PATH]
Manifest section: [SECTION]

Read repository instructions, docs/codebase_domains.md, relevant architecture docs, and the complete improve-codebase-readability skill and references. Establish the domain's major reading tasks and code paths across its scope and key files, and trace them through callers, dependencies, and tests. Apply the change-context, reading-walkthrough, responsibility, state, ordering, abstraction-level, naming, and extraction tests. Examine the entire domain and leave no area unexplored.

Record under [SECTION] only:
- areas examined, with concrete code or reading-walkthrough evidence;
- every credible candidate, with an accept, reject, or defer decision and reason;
- reading task, current reading walkthrough, friction category, and evidence;
- proposed readability improvement and the context it would make easier to understand;
- preserved behaviour and ownership;
- reading-task verification and test impact;
- files and domains involved;
- stable domain slug;
- status `planned` for accepted candidates, in execution order.

Before recording a candidate, read the other manifest sections. If another section already records the same opportunity, reference that entry instead of recording a duplicate.

Discovery only. Edit only [SECTION] of [MANIFEST_PATH]. Do not change other sections, production code, Git state, or commits. Run the Markdown residue scan and git diff --check for the manifest. Return the section, accepted candidates, and counts of rejected and deferred candidates.
```

## Planning agent

```text
Explore codebase readability candidate [INDEX]: [TITLE].

Repository: [ROOT]
Manifest entry: [ENTRY]
Output file: [PLAN_PATH]

Read repository instructions, the manifest, relevant architecture/domain docs, and the complete improve-codebase-readability vocabulary and readability-design references. Trace the reading task, current implementation, callers, helpers, and tests. Apply the change-context, reading-walkthrough, responsibility, state, ordering, abstraction-level, naming, and extraction tests.

Write a standalone solution plan containing:
- reading task and current reading walkthrough;
- concrete evidence and friction category;
- constraints, preserved behaviour, and ownership;
- recommended changes to names, control flow, state, grouping, or contracts within the current architecture;
- responsibilities, state, abstraction levels, ordering, effects, and error modes;
- exact phased file and caller migration;
- added or removed calls, contracts, and navigation, and their effect on the complete reading task;
- tests to add, replace, and delete;
- reading-task verification and correctness gate;
- alternatives, risks, remaining comprehension burden, decisions, and acceptance criteria.

Planning only. Edit only [PLAN_PATH]. Do not change production code, other plans, Git state, or commits. Planning detail may exceed source-file line guidance when it prevents rediscovery; remove repetition. Run the Markdown residue scan and git diff --check for the file. Return the path, core recommendation, and verification.
```

## Implementer X

```text
Implement accepted codebase readability plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Manifest: [MANIFEST_PATH]
Baseline HEAD: [SHA]
Baseline reading walkthrough: [EVIDENCE]
Pre-existing user paths: [PATHS]
Plan-owned scope: [SCOPE]
Required reading-task verification: [COMMAND_OR_METHOD]
Required focused checks: [COMMAND]

Read repository instructions and every document required by the plan. Work only in [WORKTREE_PATH]. Inspect current status/diff before editing. Implement the plan end to end using the simplest repo-native design. Preserve unrelated and pre-existing changes, runtime behaviour, domain meaning, and accepted ownership. Update affected durable docs and add regression coverage where behavioural invariants lack protection. Walk the same reading task before and after the change, including relevant callers and helpers. If repository reality invalidates a material plan decision, stop and report the evidence before diverging.

Run targeted checks while working, then run [COMMAND_OR_METHOD] and [COMMAND] against the final tree. Fix failures within scope. Report the reading walkthrough with code references separately from exact focused-check commands and key output. Explain how the reading task became easier, accounting for added calls, contracts, and navigation. Do not run the full gate. Do not stage, commit, push, rewrite history, or perform destructive Git operations. Return changed files, acceptance evidence, reading-task verification, focused-check result, and any blocker.
```

## Reviewer Y

```text
Review the implementation of codebase readability plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Baseline HEAD: [SHA]
Baseline reading walkthrough: [EVIDENCE]
Plan-owned diff/files: [DIFF_OR_PATHS]
Repository instructions: [INSTRUCTION_PATHS]
Reported reading-task verification: [EVIDENCE]
Reported focused-check evidence: [EVIDENCE]

Review read-only. Do not edit, stage, commit, or push. Review only the plan-owned diff. Read surrounding code only to judge the change. Report only defects in changed code or defects the change introduces; pre-existing issues outside the diff are out of scope. Verify the implementation against the accepted plan, reading task, friction evidence, preserved behaviour and ownership, repository contracts, callers, tests, migrations, runtime behaviour, and failure modes. Repeat the reading task against the baseline and final code. Assess the claimed improvement yourself, including added calls, contracts, and navigation. Verify that the walkthrough addresses the identified friction and that correctness evidence protects the preserved behaviour. Inspect the actual diff and relevant surrounding code. Run read-only or non-mutating checks when useful.

Report findings first, ordered critical, high, medium, low. For each finding include:
- severity;
- exact file and tight line range;
- concrete failure mode or violated contract;
- required outcome;
- evidence sufficient for the implementer to reproduce or rebut it.

Use critical for security/data-loss/destructive-deploy failures; high for correctness/regression/contract/ownership/material-readability-regression/acceptance failures; medium for plausible cognitive-load/navigation/contract/documentation/observability/test impact; low for localized quality issues. Avoid speculative findings and formatting issues already enforced mechanically. If no findings exist, say so explicitly and list any residual verification risk.
```

## Resolution feedback to X

```text
Resolve the independent review for plan [INDEX]: [TITLE].

Review findings:
[FINDINGS]

Address every finding with a recorded disposition: fix it, or rebut it with concrete code/test/reading-walkthrough evidence proving it is not a real issue. Deferral is not a disposition.

Bare disagreement is insufficient. Preserve the accepted plan, runtime behaviour, domain meaning, accepted ownership, and unrelated user changes. Add or adjust regression coverage for valid behavioural findings. After the final edit, rerun targeted checks, the reading-task verification [COMMAND_OR_METHOD], and the focused checks [COMMAND]. Do not run the full gate, commit, or push.

Return, for each finding: disposition, rationale, files changed, and verification. Include exact final reading-task and focused-check evidence.
```

## Closure review with Y

```text
Verify closure of the review findings for plan [INDEX]: [TITLE].

Original findings:
[FINDINGS]

Implementer dispositions:
[DISPOSITIONS]

Final diff: [DIFF_OR_PATHS]
Final reading-task verification: [EVIDENCE]
Final focused-check evidence: [EVIDENCE]

Review read-only. Confirm whether each finding is fixed or convincingly rebutted. Check for regressions introduced by the resolution and confirm the readability improvement still holds for the complete reading task. Report only remaining or new findings, with severity and evidence. State explicitly when all findings are closed. Do not edit, stage, commit, or push.
```

## Main-agent acceptance record

For each plan, retain these facts until commitment:

```text
Plan: [INDEX] [TITLE]
Baseline: [SHA]
Worktree: [WORKTREE_PATH]
Reading task: [TASK]
Friction and category: [FRICTION + CATEGORY]
Baseline reading walkthrough: [EVIDENCE]
Implementer: [AGENT]
Reviewer: [AGENT]
Files: [PATHS]
Initial reading-task verification: [COMMAND_OR_METHOD + RESULT]
Initial focused checks: [COMMAND + RESULT]
Findings: [SEVERITY + SUMMARY]
Dispositions: [FIXED / REBUTTED + RATIONALE]
Closure: [RESULT]
Final reading-task verification: [COMMAND_OR_METHOD + RESULT]
Final focused checks: [COMMAND + RESULT]
Commit: readability([DOMAIN]): [MESSAGE]
Commit SHA: [SHA]
```
