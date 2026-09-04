---
read_when: Read before spawning planning, implementation, review, resolution, or closure agents for the streamline-codebase workflow.
last_updated: 2026-08-31
---

# Agent Prompt Contracts

Replace bracketed fields with task-specific facts. Give agents repository paths and raw artifacts. Avoid supplying expected conclusions.

## Planning agent

```text
Explore codebase ergonomics candidate [INDEX]: [TITLE].

Repository: [ROOT]
Manifest entry: [ENTRY]
Output file: [PLAN_PATH]

Read repository instructions, the manifest, relevant architecture/domain docs, and the complete improve-codebase-ergonomics vocabulary and ergonomic-design references. Trace the representative task, current organization or usage surface, callers, and tests. Apply the task-walkthrough, canonical-path, organization, discoverability, ceremony, choice, common-path, and residue tests.

Write a standalone solution plan containing:
- representative task and current task walkthrough;
- concrete evidence and friction category;
- constraints, preserved behaviour, and ownership;
- recommended organization or usage surface and canonical path;
- required choices, defaults, ordering, and error modes;
- exact phased file and caller migration;
- obsolete paths, aliases, helpers, exports, and documentation to delete;
- tests to add, replace, and delete;
- representative-task verification and correctness gate;
- alternatives, risks, residual friction, decisions, and acceptance criteria.

Planning only. Edit only [PLAN_PATH]. Do not change production code, other plans, Git state, or commits. Planning detail may exceed source-file line guidance when it prevents rediscovery; remove repetition. Run the Markdown residue scan and git diff --check for the file. Return the path, core recommendation, and verification.
```

## Implementer X

```text
Implement accepted codebase ergonomics plan [INDEX]: [TITLE].

Repository: [ROOT]
Plan: [PLAN_PATH]
Manifest: [MANIFEST_PATH]
Baseline HEAD: [SHA]
Baseline task walkthrough: [EVIDENCE]
Pre-existing user paths: [PATHS]
Plan-owned scope: [SCOPE]
Required representative-task verification: [COMMAND_OR_METHOD]
Required full gate: [COMMAND]

Read repository instructions and every document required by the plan. Inspect current status/diff before editing. Implement the plan end to end using the simplest repo-native design. Preserve unrelated and pre-existing changes, runtime behaviour, domain meaning, and accepted ownership. Migrate representative callers and delete obsolete paths and residue. Update affected durable docs and regression coverage. If repository reality invalidates a material plan decision, stop and report the evidence before diverging.

Run targeted checks while working, then run [COMMAND_OR_METHOD] and [COMMAND] against the final tree. Fix failures within scope. Report exact commands and key output, including evidence that the representative task became easier and the canonical path is singular. Do not stage, commit, push, rewrite history, or perform destructive Git operations. Return changed files, acceptance evidence, representative-task verification, gate result, and any blocker.
```

## Reviewer Y

```text
Review the implementation of codebase ergonomics plan [INDEX]: [TITLE].

Repository: [ROOT]
Plan: [PLAN_PATH]
Baseline HEAD: [SHA]
Baseline task walkthrough: [EVIDENCE]
Plan-owned diff/files: [DIFF_OR_PATHS]
Repository instructions: [INSTRUCTION_PATHS]
Reported representative-task verification: [EVIDENCE]
Reported gate evidence: [EVIDENCE]

Review read-only. Do not edit, stage, commit, or push. Verify the implementation against the accepted plan, representative task, friction evidence, canonical path, preserved behaviour and ownership, repository contracts, callers, tests, migrations, runtime behaviour, and failure modes. Confirm that obsolete paths and residue are removed and that the verification surface matches the claimed friction reduction. Inspect the actual diff and relevant surrounding code. Run read-only or non-mutating checks when useful.

Report findings first, ordered critical, high, medium, low. For each finding include:
- severity;
- exact file and tight line range;
- concrete failure mode or violated contract;
- required outcome;
- evidence sufficient for the implementer to reproduce or rebut it.

Use critical for security/data-loss/destructive-deploy failures; high for correctness/regression/contract/ownership/competing-canonical-path/false-ergonomics-claim/material-residue/acceptance failures; medium for plausible discoverability/ceremony/cognitive-load/documentation/observability/test impact; low for localized quality issues. Avoid speculative findings and formatting issues already enforced mechanically. If no findings exist, say so explicitly and list any residual verification risk.
```

## Resolution feedback to X

```text
Resolve the independent review for plan [INDEX]: [TITLE].

Review findings:
[FINDINGS]

Address every finding with a recorded disposition.
- Critical/high: fix it, or rebut it with concrete code/test/task-walkthrough evidence proving it is not a real issue.
- Medium/low: fix it, defer it with a load-bearing technical rationale, or rebut it as a false positive.

Bare disagreement is insufficient. Preserve the accepted plan, runtime behaviour, domain meaning, accepted ownership, and unrelated user changes. Add or adjust regression coverage for valid behavioural findings. After the final edit, rerun targeted checks, the representative-task verification [COMMAND_OR_METHOD], and the full gate [COMMAND]. Do not commit or push.

Return, for each finding: disposition, rationale, files changed, and verification. Include exact final representative-task and full-gate evidence.
```

## Closure review with Y

```text
Verify closure of the critical/high review findings for plan [INDEX]: [TITLE].

Original findings:
[FINDINGS]

Implementer dispositions:
[DISPOSITIONS]

Final diff: [DIFF_OR_PATHS]
Final representative-task verification: [EVIDENCE]
Final gate evidence: [EVIDENCE]

Review read-only. Confirm whether each critical/high finding is fixed or convincingly rebutted. Check for regressions introduced by the resolution and confirm the ergonomic improvement still holds with one canonical path and no material residue. Report only remaining or new findings, with severity and evidence. State explicitly when all critical/high findings are closed. Do not edit, stage, commit, or push.
```

## Main-agent acceptance record

For each plan, retain these facts until commitment:

```text
Plan: [INDEX] [TITLE]
Baseline: [SHA]
Representative task: [TASK]
Friction and category: [FRICTION + CATEGORY]
Baseline task walkthrough: [EVIDENCE]
Implementer: [AGENT]
Reviewer: [AGENT]
Files: [PATHS]
Initial representative-task verification: [COMMAND_OR_METHOD + RESULT]
Initial full gate: [COMMAND + RESULT]
Findings: [SEVERITY + SUMMARY]
Dispositions: [FIXED / REBUTTED / DEFERRED + RATIONALE]
Closure: [RESULT]
Final representative-task verification: [COMMAND_OR_METHOD + RESULT]
Final full gate: [COMMAND + RESULT]
Commit: ergonomics([DOMAIN]): [MESSAGE]
Commit SHA: [SHA]
```
