---
name: code-quality-reviewer
description: Review code for quality, maintainability, and best practices. Use when asked to do a code review, after implementing or refactoring features, before commits/releases, or when checking robustness/readability of existing code.
---

# Code Quality Reviewer

## Overview

Provide structured, constructive code reviews focused on clean code, maintainability, and long-term safety.

## Review Workflow

1. Identify the scope and key files under review; load relevant code and tests.
2. Evaluate code against the quality checklist and robustness checks below.
3. Report findings ordered by severity with precise file references.
4. Suggest concrete improvements with minimal, focused examples.
5. Call out strong practices and end with prioritized recommendations.

## Quality Checklist

- Assess naming clarity and consistency.
- Check for single-responsibility functions and cohesive modules.
- Identify duplication and suggest DRY refactors.
- Flag overly complex logic and simplify when possible.
- Verify separation of concerns and appropriate abstractions.

## Robustness and Edge Cases

- Confirm error handling at failure points.
- Verify input validation and defensive checks.
- Handle null/undefined and empty-collection cases.
- Verify boundary conditions and off-by-one risks.
- Confirm errors are propagated or surfaced appropriately.

## Readability and Maintainability

- Check structure, organization, and control flow clarity.
- Encourage purposeful comments; avoid noisy or obvious ones.
- Replace magic numbers/strings with named constants.
- Verify consistent formatting and style.

## Best Practices

- Check for SOLID adherence where applicable.
- Recommend appropriate patterns without overengineering.
- Consider performance implications of key hot paths.
- Review security posture (sanitization, sensitive data handling).

## Output Format

- Start with a brief overall quality summary.
- Group findings by severity (critical, important, minor).
- Include file references and line hints when possible.
- Provide concrete fixes or examples for each issue.
- Highlight positives and end with actionable next steps.
