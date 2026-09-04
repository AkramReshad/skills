---
name: conventions-maintainer
description: Create or update repository conventions docs (at repo root (CONVENTIONS.md)) with terse, domain-based patterns, anti-patterns, and guardrails for AI agents. Use when asked to document repo paradigms, coding patterns, architectural constraints, or onboarding guidance that should be read before implementation.
---

# Conventions Maintainer

## Overview
Create a compact conventions doc that captures repo-specific patterns and guardrails. Prioritize actionable bullets over explanations.

## Workflow
1. Read architecture overview first.
2. Gather only repo-specific rules from docs/notes/tests (skip generic Python/AWS advice).
3. Write/update `<repo>/CONVENTIONS.md` as domain sections with flat bullets.
4. Keep wording imperative and short.
5. Validate that bullets are actionable and non-contradictory.

## Output Contract
- Keep concise: no long prose blocks.
- Organize by domain (example: `api routes`, `core services`, `models/db`, `tests`, `auth`, `analytics/billing`).
- For each domain, include:
  - preferred patterns
  - avoid/anti-patterns
  - naming/contract rules
- Add two cross-cutting sections:
  - `Do Not Infer` (common agent mistakes)
  - `Pre-Edit Checklist` (5-8 bullets)

## Quality Bar
- Every bullet must be testable in code review.
- No duplicated guidance from architecture docs.
- No stale specifics unless tied to current behavior.
- Prefer stable contracts over implementation trivia.

## Update Rules
- If behavior/API contract changes, update conventions in same change.
- If uncertain, point to exact source docs instead of inventing rules.
- Keep file under ~250 lines.

## Reference
Use [references/domain-checklist.md](references/domain-checklist.md) as a drafting checklist.
