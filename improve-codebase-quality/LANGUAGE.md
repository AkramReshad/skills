# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly. Preserve canonical repo-local and domain vocabulary.

## Terms

**Domain**
A review partition with a name, persona, scope, and anchor paths. Existing domain configuration is canonical when present.

**Issue**
A defect or concrete quality problem supported by current code, a representative trigger, and a consequence. Retain every validated issue regardless of the number already found.

**Evidence**
The code, execution path, or targeted check establishing an issue and its consequence. Distinguish demonstrated behaviour from an inference or an unverified suspicion.

**Severity**
The impact and likelihood of an issue in representative use. State the affected behaviour and conditions; category alone does not determine severity.

**Non-issue**
An explicitly accepted concern with a reason and revisit trigger. A reviewer cannot accept a trade-off on the user's behalf.

**Verification**
Evidence that a proposed fix resolves its issue while preserving required behaviour. Match checks to the failure mechanism.

## Principles

- **Complete domain coverage.** Review every domain and every file in its scope; disclose unread areas and blocked verification.
- **Validate every finding.** Trace current code, callers, and relevant dependencies before retaining an issue or proposing a fix.
- **Persistent issue hygiene.** Keep valid issues, remove resolved or disproven issues, reconcile duplicates, and preserve accepted non-issues.
- **Verification matches the mechanism.** Specify observable checks for the failure and required preserved behaviour.
- **Review artifacts stay local.** Keep `code_review/` ignored and uncommitted.
