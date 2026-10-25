---
read_when: Read before spawning discovery, planning, implementation, review, resolution, or closure agents for the align-codebase workflow.
last_updated: 2026-10-23
---

# Agent Prompt Contracts

Replace bracketed fields with task-specific facts. Give agents repository paths and raw artifacts. Avoid supplying expected conclusions.

## Discovery agent

```text
Discover codebase contract-consistency opportunities in domain [INDEX]: [DOMAIN].

Repository: [ROOT]
Domain row: [ROW]
Manifest: [MANIFEST_PATH]
Manifest section: [SECTION]

Read repository instructions, docs/codebase_domains.md, relevant architecture docs, and the complete improve-codebase-contracts skill and references. Establish the domain's boundary contracts, with their producers and consumers, across its scope and key files, and trace them through callers, dependencies, and tests. Apply the contract-trace, source-of-truth, field, optionality, enum, error-shape, runtime-parse, version, and unused-field tests. Examine the entire domain and leave no area unexplored.

Record under [SECTION] only:
- areas examined, with concrete code or contract-trace evidence;
- every credible candidate, with an accept, reject, or defer decision and reason;
- boundary contract, producer, consumers, drift category, and evidence;
- proposed consumer correction and source of truth;
- preserved producer output and ownership;
- contract verification and test impact;
- files and domains involved;
- stable domain slug;
- status `planned` for accepted candidates, in execution order.

Before recording a candidate, read the other manifest sections. If another section already records the same opportunity, reference that entry instead of recording a duplicate.

Discovery only. Edit only [SECTION] of [MANIFEST_PATH]. Do not change other sections, production code, Git state, or commits. Run the Markdown residue scan and git diff --check for the manifest. Return the section, accepted candidates, and counts of rejected and deferred candidates.
```

## Planning agent

```text
Explore codebase contract-consistency candidate [INDEX]: [TITLE].

Repository: [ROOT]
Manifest entry: [ENTRY]
Output file: [PLAN_PATH]

Read repository instructions, the manifest, relevant architecture/domain docs, and the complete improve-codebase-contracts vocabulary and contracts-design references. Trace the boundary contract, the producer's definition and output, every consumer, callers, and tests. Apply the contract-trace, source-of-truth, field, optionality, enum, error-shape, runtime-parse, version, and unused-field tests.

Write a standalone solution plan containing:
- boundary contract and current contract trace;
- concrete evidence and drift category;
- constraints, preserved producer output, and ownership;
- source of truth and derivation;
- recommended consumer correction and affected implementation;
- required and nullable fields, value sets, error payloads, and versions;
- exact phased file and caller migration;
- duplicated definitions, stale fields, and documentation to remove;
- tests to add, replace, and delete;
- contract verification and correctness gate;
- alternatives, risks, residual drift, decisions, and acceptance criteria.

Planning only. Edit only [PLAN_PATH]. Do not change production code, other plans, Git state, or commits. Planning detail may exceed source-file line guidance when it prevents rediscovery; remove repetition. Run the Markdown residue scan and git diff --check for the file. Return the path, core recommendation, and verification.
```

## Implementer X

```text
Implement accepted codebase contract-consistency plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Manifest: [MANIFEST_PATH]
Baseline HEAD: [SHA]
Baseline contract trace: [EVIDENCE]
Pre-existing user paths: [PATHS]
Plan-owned scope: [SCOPE]
Required contract verification: [COMMAND_OR_METHOD]
Required focused checks: [COMMAND]

Read repository instructions and every document required by the plan. Work only in [WORKTREE_PATH]. Inspect current status/diff before editing. Implement the plan end to end using the simplest repo-native design. Preserve unrelated and pre-existing changes, producer output, domain meaning, and accepted ownership. Remove duplicated definitions the plan replaces. Update affected durable docs and regression coverage. If repository reality invalidates a material plan decision, stop and report the evidence before diverging.

Run targeted checks while working, then run [COMMAND_OR_METHOD] and [COMMAND] against the final tree. Fix failures within scope. Report exact commands and key output, including evidence that each targeted consumer parses real producer output and agrees field by field. Do not run the full gate. Do not stage, commit, push, rewrite history, or perform destructive Git operations. Return changed files, acceptance evidence, contract verification, focused-check result, and any blocker.
```

## Reviewer Y

```text
Review the implementation of codebase contract-consistency plan [INDEX]: [TITLE].

Repository: [ROOT]
Worktree: [WORKTREE_PATH]
Plan: [PLAN_PATH]
Baseline HEAD: [SHA]
Baseline contract trace: [EVIDENCE]
Plan-owned diff/files: [DIFF_OR_PATHS]
Repository instructions: [INSTRUCTION_PATHS]
Reported contract verification: [EVIDENCE]
Reported focused-check evidence: [EVIDENCE]

Review read-only. Do not edit, stage, commit, or push. Review only the plan-owned diff. Read surrounding code only to judge the change. Report only defects in changed code or defects the change introduces; pre-existing issues outside the diff are out of scope. Verify the implementation against the accepted plan, boundary contract, drift evidence, source of truth, preserved producer output and ownership, repository contracts, callers, tests, migrations, runtime behaviour, and failure modes. Confirm that replaced definitions are removed and that the verification parses real producer output with the consumer's schema or parser. Inspect the actual diff and relevant surrounding code. Run read-only or non-mutating checks when useful.

Report findings first, ordered critical, high, medium, low. For each finding include:
- severity;
- exact file and tight line range;
- concrete failure mode or violated contract;
- required outcome;
- evidence sufficient for the implementer to reproduce or rebut it.

Use critical for security/data-loss/destructive-deploy failures; high for correctness/regression/contract/ownership/remaining-drift/competing-source-of-truth/false-contract-claim/acceptance failures; medium for plausible runtime-parse/versioning/documentation/observability/test impact; low for localized quality issues. Avoid speculative findings and formatting issues already enforced mechanically. If no findings exist, say so explicitly and list any residual verification risk.
```

## Resolution feedback to X

```text
Resolve the independent review for plan [INDEX]: [TITLE].

Review findings:
[FINDINGS]

Address every finding with a recorded disposition: fix it, or rebut it with concrete code/test/contract-trace evidence proving it is not a real issue. Deferral is not a disposition.

Bare disagreement is insufficient. Preserve the accepted plan, producer output, domain meaning, accepted ownership, and unrelated user changes. Add or adjust regression coverage for valid behavioural findings. After the final edit, rerun targeted checks, the contract verification [COMMAND_OR_METHOD], and the focused checks [COMMAND]. Do not run the full gate, commit, or push.

Return, for each finding: disposition, rationale, files changed, and verification. Include exact final contract-verification and focused-check evidence.
```

## Closure review with Y

```text
Verify closure of the review findings for plan [INDEX]: [TITLE].

Original findings:
[FINDINGS]

Implementer dispositions:
[DISPOSITIONS]

Final diff: [DIFF_OR_PATHS]
Final contract verification: [EVIDENCE]
Final focused-check evidence: [EVIDENCE]

Review read-only. Confirm whether each finding is fixed or convincingly rebutted. Check for regressions introduced by the resolution and confirm every targeted consumer still agrees with real producer output. Report only remaining or new findings, with severity and evidence. State explicitly when all findings are closed. Do not edit, stage, commit, or push.
```

## Main-agent acceptance record

For each plan, retain these facts until commitment:

```text
Plan: [INDEX] [TITLE]
Baseline: [SHA]
Worktree: [WORKTREE_PATH]
Boundary contract: [CONTRACT]
Drift and category: [DRIFT + CATEGORY]
Baseline contract trace: [EVIDENCE]
Implementer: [AGENT]
Reviewer: [AGENT]
Files: [PATHS]
Initial contract verification: [COMMAND_OR_METHOD + RESULT]
Initial focused checks: [COMMAND + RESULT]
Findings: [SEVERITY + SUMMARY]
Dispositions: [FIXED / REBUTTED + RATIONALE]
Closure: [RESULT]
Final contract verification: [COMMAND_OR_METHOD + RESULT]
Final focused checks: [COMMAND + RESULT]
Commit: contracts([DOMAIN]): [MESSAGE]
Commit SHA: [SHA]
```
