---
name: handoff
description: Create a concise handoff document so another agent can continue work with the objective, current state, significant attempts, and next steps preserved.
---

# Handoff

Write a Markdown handoff that lets another agent continue without access to the conversation. If arguments specify the next session's focus, tailor the document accordingly while preserving relevant constraints and unfinished work.

## Writing and Placement

Prioritize truth, succinctness, and standalone clarity:

- Support material claims with the conversation, repository, or referenced evidence. Distinguish observations, decisions, and tentative explanations; leave unknowns explicit.
- Write the shortest document that preserves what is needed to continue. Remove repetition, filler, and empty sections.
- Make the content understandable without the prior conversation. State decisions and findings directly, define unfamiliar project terms, and avoid phrases such as "as discussed."

Preserve the conclusions needed to continue and link to supporting specs, plans, issues, commits, diffs, or logs. Avoid reproducing entire artifacts. Include history only when it affects what the next agent should do.

## Suggested Document Structure

Use a descriptive task title and these sections as a starting point. Combine or omit sections that add no useful information; include the relevant task-specific details below.

- **Objective and constraints:** The current agreed objective, completion criteria, relevant user decisions, and scope or authorization limits that affect continuation.
- **Current state:** Established findings, changes made, and where work stopped. Include the repository, branch, relevant uncommitted changes, or environment details when needed to locate or interpret the work. Flag state that has not been checked recently.
- **Continuation:** Remaining work in useful order, blockers, unresolved decisions, and the next concrete action. Distinguish agreed next steps from recommendations.
- **References:** Paths or URLs to the authoritative artifacts, with enough context to explain what each supports. Use paths the successor can resolve.
- **Suggested skills:** Available skills relevant to the remaining work and a brief reason to use each. Identify required prerequisites when known.

## Troubleshooting and Triage

Preserve the observed symptom and reproduction conditions. For significant attempts, capture:

**Hypothesis → action → observed result → implication.**

Include the command, configuration, or evidence reference needed to interpret the result. Distinguish an approach that failed, a hypothesis contradicted by evidence, and an experiment that was blocked or inconclusive. Record what would make retrying useful, such as a changed prerequisite or environment.

Example: Increasing the timeout to 60 seconds produced the same failure after two seconds. This suggests that setting does not control this failure; inspect the upstream deadline next. Link the relevant logs.

Keep unresolved hypotheses explicit. Retain failed attempts that would otherwise be repeated or that materially narrow the investigation.

## Feature Work

Distinguish **implemented**, **verified**, and **remaining** work. Record which checks ran and their outcomes, including failed or unrun checks that affect readiness. Identify partial changes, relevant uncommitted work, and unresolved design or integration decisions.

Reference existing plans and acceptance criteria, and summarize progress against them. Preserve the reason for consequential implementation choices when it is not captured elsewhere.

## Final Check

Confirm the successor can locate the work, understand its status and uncertainty, avoid repeating significant attempts without cause, and identify the next useful action. Check that claims and references are supported and no secrets remain.
